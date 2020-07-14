# -*- coding: utf-8 -*-

"""Implementation of HttpTagSubscription."""

import datetime
import weakref
from typing import Iterable, List, Optional

from systemlink.clients import core, tag as tbase
from systemlink.clients.core._internal._http_client import HttpClient
from systemlink.clients.core._internal._timestamp_utilities import TimestampUtilities
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer
from systemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)
from systemlink.clients.tag._core._serialized_tag_with_aggregates_reader import (
    SerializedTagWithAggregatesReader,
)
from typing_extensions import final


@final
class HttpTagSubscription(tbase.TagSubscription):
    _DEFAULT_POLLING_INTERVAL_MILLISECONDS = 5000.0

    __MAGIC = object()

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'HttpTagSubscription' is not an acceptable base type")

    @classmethod
    def create(
        cls,
        client: HttpClient,
        paths: Iterable[str],
        update_timer: Optional[ManualResetTimer] = None,
        heartbeat_timer: Optional[ManualResetTimer] = None,
    ) -> "HttpTagSubscription":
        """Create an :class:`HttpTagSubscription` with a custom heartbeat timer for testing purposes.

        Args:
            client: The HTTP client object for communicating with the server.
            paths: The tag path queries to include in the subscription.
            update_timer: A timer for polling for updates on the server, or None to use
                a default timer.
            heartbeat_timer: A timer for sending a heartbeat to keep the subscription
                alive, or None to use a default timer.

        Returns:
            The created subscription.

        Raises:
            ValueError: if ``paths`` is None.
            ApiException: if the API call fails.
        """
        subscription = HttpTagSubscription(
            cls.__MAGIC, client, paths, update_timer, heartbeat_timer
        )
        subscription._initialize()
        return subscription

    @classmethod
    async def create_async(
        cls,
        client: HttpClient,
        paths: Iterable[str],
        update_timer: Optional[ManualResetTimer] = None,
        heartbeat_timer: Optional[ManualResetTimer] = None,
    ) -> "HttpTagSubscription":
        """Asynchronously create an :class:`HttpTagSubscription` with a custom heartbeat timer for testing purposes.

        Args:
            client: The HTTP client object for communicating with the server.
            paths: The tag path queries to include in the subscription.
            update_timer: A timer for polling for updates on the server, or None to use
                a default timer.
            heartbeat_timer: A timer for sending a heartbeat to keep the subscription
                alive, or None to use a default timer.

        Returns:
            A task representing the asynchronous operation. On completion, contains the
            created subscription.

        Raises:
            ValueError: if ``paths`` is None.
            ApiException: if the API call fails.
        """
        subscription = HttpTagSubscription(
            cls.__MAGIC, client, paths, update_timer, heartbeat_timer
        )
        await subscription._initialize_async()
        return subscription

    def __init__(
        self,
        magic: object,
        client: HttpClient,
        paths: Iterable[str],
        update_timer: Optional[ManualResetTimer] = None,
        heartbeat_timer: Optional[ManualResetTimer] = None,
    ) -> None:
        assert (
            magic is self.__MAGIC
        ), "Do not construct an HttpTagSubscription directly. Use create() instead."
        super().__init__(paths, heartbeat_timer)
        self._api = client.at_uri("/nitag/v2/subscriptions")
        if update_timer is not None:
            self._update_timer = update_timer
        else:
            self._update_timer = ManualResetTimer(
                datetime.timedelta(
                    milliseconds=self._DEFAULT_POLLING_INTERVAL_MILLISECONDS
                )
            )
            # _exit_stack is instantiated in the base class
            self._exit_stack.enter_context(self._update_timer)

        callback_ref = weakref.WeakMethod(self._update_timer_elapsed)  # type: ignore

        def callback() -> None:
            actual_callback = callback_ref()  # type: ignore
            if actual_callback:
                actual_callback()

        self._update_timer_handler = callback
        self._update_timer.elapsed += self._update_timer_handler
        self._token = None  # type: Optional[str]

    # Base class implementation is sufficient:
    #   def __enter__(self):
    #   async def __aenter__(self):
    #   def __exit__(self, exc_type, exc, traceback):
    #   async def __aexit__(self, exc_type, exc, traceback):

    def _close_internal(self) -> None:
        if self._token is None:
            return

        try:
            self._update_timer.stop()
            self._update_timer.elapsed -= self._update_timer_handler
            self._api.delete("/{id}", params={"id": self._token})
            self._token = None
        except core.ApiException:
            pass

    async def _close_internal_async(self) -> None:
        if self._token is None:
            return

        try:
            self._update_timer.stop()
            self._update_timer.elapsed -= self._update_timer_handler
            await self._api.as_async.delete("/{id}", params={"id": self._token})
            self._token = None
        except core.ApiException:
            pass

    def _create_subscription_on_server(self, paths: List[str]) -> None:
        response, http_response = self._api.post(
            "", data={"updatesOnly": True, "tags": paths}
        )

        if response is None or response.get("subscriptionId") is None:
            raise tbase.TagManager.invalid_response(http_response)

        token = response["subscriptionId"]

        # We only want to expose real changes to tags, but the subscription service
        # initially sends metadata and current values for every tag in the subscription.
        # For our API, we want clients to query using a selection prior to creating the
        # subscription if they want current information.
        self._api.get("/{id}/values/current", params={"id": token})
        self._token = token
        self._update_timer.start()

    async def _create_subscription_on_server_async(self, paths: List[str]) -> None:
        response, http_response = await self._api.as_async.post(
            "", data={"updatesOnly": True, "tags": paths}
        )

        if response is None or response.get("subscriptionId") is None:
            raise tbase.TagManager.invalid_response(http_response)

        token = response["subscriptionId"]

        # We only want to expose real changes to tags, but the subscription service
        # initially sends metadata and current values for every tag in the subscription.
        # For our API, we want clients to query using a selection prior to creating the
        # subscription if they want current information.
        await self._api.as_async.get("/{id}/values/current", params={"id": token})
        self._token = token
        self._update_timer.start()

    def _send_heartbeat(self) -> None:
        assert self._token is not None
        self._api.put("/{id}/heartbeat", params={"id": self._token})

    def _update_timer_elapsed(self) -> None:
        try:
            token = self._token
            if token is None:
                return

            try:
                response, _ = self._api.get(
                    "/{id}/values/current", params={"id": token}
                )
            except core.ApiException:
                return

            if response is None:
                return

            subscriptions = response.get("subscriptionUpdates")
            if subscriptions is None:
                return

            for subscription in subscriptions:
                if subscription is None:
                    continue

                updates = subscription.get("updates")
                if updates is None:
                    continue

                for update in updates:
                    if update is None:
                        continue

                    tag = update.get("tag")
                    timestamp = update.get("timestamp")
                    if tag is None or timestamp is None:
                        continue

                    tag = tbase.TagData.from_json_dict(tag)
                    try:
                        tag.validate_path()
                    except ValueError:
                        continue
                    aggregates = update.get("aggregates") or {}
                    if tag.data_type == tbase.DataType.UNKNOWN:
                        self._on_tag_changed(tag, None)
                    else:
                        value = SerializedTagWithAggregates(
                            tag.path,
                            tag.data_type,
                            update.get("value"),
                            TimestampUtilities.str_to_datetime(timestamp),
                            aggregates.get("count"),
                            aggregates.get("min"),
                            aggregates.get("max"),
                            (
                                float(aggregates["avg"])
                                if aggregates.get("avg") is not None
                                else None
                            ),
                        )
                        reader = tbase.TagValueReader(
                            SerializedTagWithAggregatesReader(value), tag
                        )  # type: tbase.TagValueReader
                        self._on_tag_changed(tag, reader)
        finally:
            self._update_timer.start()
