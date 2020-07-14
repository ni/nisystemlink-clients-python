# -*- coding: utf-8 -*-

"""Implementation of HttpTagSelection."""

import datetime
from typing import Any, Awaitable, Callable, List, Optional, Sequence, Tuple, TypeVar

from systemlink.clients import core, tag as tbase
from systemlink.clients.core._internal._http_client import HttpClient, HttpResponse
from systemlink.clients.core._internal._timestamp_utilities import TimestampUtilities
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer
from systemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)
from systemlink.clients.tag._http._http_tag_subscription import HttpTagSubscription
from typing_extensions import final


T = TypeVar("T")


@final
class HttpTagSelection(tbase.TagSelection):
    def __init_subclass__(cls) -> None:
        raise TypeError("type 'HttpTagSelection' is not an acceptable base type")

    def __init__(
        self,
        client: HttpClient,
        tags: Sequence[tbase.TagData],
        *,
        _paths: Optional[Sequence[str]] = None
    ) -> None:
        """Initialize a selection using existing data.

        Args:
            client: The HTTP client object for communicating with the server.
            tags: The tags to store in the selection.

        Raises:
            ValueError: if ``tags`` contains tags that are None or have invalid paths.
            ValueError: if ``tags`` contains duplicate tags.
            ValueError: if ``tags`` is None.
        """
        super().__init__(tags, _paths)
        self._client = client
        self._api = client.at_uri("/nitag/v2/selections")
        self._selection_stale = False
        self._token = None  # Optional[str]

    @classmethod
    def open(cls, client: HttpClient, paths: Sequence[str]) -> "HttpTagSelection":
        """Initialize a selection using queried data.

        Args:
            client: The HTTP client object for communicating with the server.
            paths: The paths used in the query.

        Returns:
            The created selection.

        Raises:
            ValueError: if ``paths`` is None.
            ValueError: if ``paths`` contains duplicate paths.
            ApiException: if the API call fails.
        """
        api = client.at_uri("/nitag/v2/selections")

        selection, http_response = api.post("", data={"searchPaths": list(paths)})

        if selection is None or selection.get("id") is None:
            raise tbase.TagManager.invalid_response(http_response)

        token = selection["id"]

        try:
            tags, http_response = api.get("/{id}/tags", params={"id": token})

            if tags is None:
                raise tbase.TagManager.invalid_response(http_response)

            selection = HttpTagSelection(
                client, [tbase.TagData.from_json_dict(t) for t in tags], _paths=paths
            )
            selection._token = token
            return selection
        except core.ApiException:
            try:
                api.delete("/{id}", params={"id": token})
            except core.ApiException:
                pass

            raise

    @classmethod
    async def open_async(
        cls, client: HttpClient, paths: Sequence[str]
    ) -> "HttpTagSelection":
        """Asynchronously initialize a selection using queried data.

        Args:
            client: The HTTP client object for communicating with the server.
            paths: The paths used in the query.

        Returns:
            A task representing the asynchronous operation. On completion, contains the
            created selection.

        Raises:
            ValueError: if ``paths`` is None.
            ValueError: if ``paths`` contains duplicate paths.
            ApiException: if the API call fails.
        """
        api = client.at_uri("/nitag/v2/selections").as_async

        selection, http_response = await api.post("", data={"searchPaths": list(paths)})

        if selection is None or selection.get("id") is None:
            raise tbase.TagManager.invalid_response(http_response)

        token = selection["id"]

        try:
            tags, http_response = await api.get("/{id}/tags", params={"id": token})

            if tags is None:
                raise tbase.TagManager.invalid_response(http_response)

            selection = HttpTagSelection(
                client, [tbase.TagData.from_json_dict(t) for t in tags], _paths=paths
            )
            selection._token = token
            return selection
        except core.ApiException:
            try:
                await api.delete("/{id}", params={"id": token})
            except core.ApiException:
                pass

            raise

    def _on_paths_changed(self) -> None:
        self._selection_stale = True

    def _close_internal(self) -> None:
        if self._token is None:
            return

        try:
            self._api.delete("/{id}", params={"id": self._token})
        except core.ApiException:
            pass

    async def _close_internal_async(self) -> None:
        if self._token is None:
            return

        try:
            await self._api.as_async.delete("/{id}", params={"id": self._token})
        except core.ApiException:
            pass

    def _create_subscription_internal(
        self, update_interval: Optional[datetime.timedelta] = None
    ) -> tbase.TagSubscription:
        update_timer = None  # type: Optional[ManualResetTimer]
        if update_interval is not None:
            update_timer = ManualResetTimer(update_interval)
        paths = set(self.paths).union(self.metadata.keys())
        return HttpTagSubscription.create(
            self._client, paths, update_timer, heartbeat_timer=None
        )

    async def _create_subscription_internal_async(
        self, update_interval: Optional[datetime.timedelta] = None
    ) -> tbase.TagSubscription:
        update_timer = None  # type: Optional[ManualResetTimer]
        if update_interval is not None:
            update_timer = ManualResetTimer(update_interval)
        paths = set(self.paths).union(self.metadata.keys())
        return await HttpTagSubscription.create_async(
            self._client, paths, update_timer, heartbeat_timer=None
        )

    def _delete_tags_from_server_internal(self) -> None:
        def fn(token: str) -> None:
            self._api.delete("/{id}/tags", params={"id": token})

        self._ensure_selection_and_call(fn)

    async def _delete_tags_from_server_internal_async(self) -> None:
        def fn(token: str) -> Awaitable[Tuple[None, HttpResponse]]:
            return self._api.as_async.delete("/{id}/tags", params={"id": token})

        await self._ensure_selection_and_call_async(fn)

    def _read_tag_metadata(self) -> List[tbase.TagData]:
        def fn(token: str) -> Tuple[Any, HttpResponse]:
            return self._api.get("/{id}/tags", params={"id": token})

        response, http_response = self._ensure_selection_and_call(fn)
        return self._handle_read_tags_metadata(response, http_response)

    async def _read_tag_metadata_async(self) -> List[tbase.TagData]:
        def fn(token: str) -> Awaitable[Tuple[Any, HttpResponse]]:
            return self._api.as_async.get("/{id}/tags", params={"id": token})

        response, http_response = await self._ensure_selection_and_call_async(fn)
        return self._handle_read_tags_metadata(response, http_response)

    def _handle_read_tags_metadata(
        self, response: List[Any], http_response: HttpResponse
    ) -> List[tbase.TagData]:
        if response is None or any(t is None for t in response):
            raise tbase.TagManager.invalid_response(http_response)

        return [tbase.TagData.from_json_dict(t) for t in response]

    def _read_tag_values(self) -> List[Optional[SerializedTagWithAggregates]]:
        def fn(token: str) -> Tuple[Any, HttpResponse]:
            return self._api.get("/{id}/values", params={"id": token})

        response, http_response = self._ensure_selection_and_call(fn)
        return self._handle_read_tags_values(response, http_response)

    async def _read_tag_values_async(
        self,
    ) -> List[Optional[SerializedTagWithAggregates]]:
        def fn(token: str) -> Awaitable[Tuple[Any, HttpResponse]]:
            return self._api.as_async.get("/{id}/values", params={"id": token})

        response, http_response = await self._ensure_selection_and_call_async(fn)
        return self._handle_read_tags_values(response, http_response)

    def _handle_read_tags_values(
        self,
        response: List[Any],
        http_response: HttpResponse,
        paths: Optional[List[str]] = None,
    ) -> List[Optional[SerializedTagWithAggregates]]:
        if response is None or any(t is None for t in response):
            raise tbase.TagManager.invalid_response(http_response)

        result = []  # type: List[Optional[SerializedTagWithAggregates]]
        for i, t in enumerate(response):
            path = paths[i] if paths else t.get("path")
            if path is None:
                raise tbase.TagManager.invalid_response(http_response)

            if not t.get("current"):
                result.append(None)
                continue

            v = t["current"].get("value", {})
            value = v.get("value")
            data_type = v.get("type")
            aggregates = t.get("aggregates") or {}
            timestamp = None  # type: Optional[datetime.datetime]
            if t["current"].get("timestamp"):
                timestamp = TimestampUtilities.str_to_datetime(
                    t["current"]["timestamp"]
                )
            if value is None or data_type is None:
                raise tbase.TagManager.invalid_response(http_response)

            result.append(
                SerializedTagWithAggregates(
                    path,
                    tbase.DataType.from_api_name(data_type),
                    value,
                    timestamp,
                    aggregates.get("count"),
                    aggregates.get("min"),
                    aggregates.get("max"),
                    (
                        float(aggregates["avg"])
                        if aggregates.get("avg") is not None
                        else None
                    ),
                )
            )
        return result

    def _read_tag_metadata_and_values(
        self,
    ) -> Tuple[List[tbase.TagData], List[Optional[SerializedTagWithAggregates]]]:
        def fn(token: str) -> Tuple[Any, HttpResponse]:
            return self._api.get("/{id}/tags-with-values", params={"id": token})

        response, http_response = self._ensure_selection_and_call(fn)
        return self._handle_read_tags_metadata_and_values(response, http_response)

    async def _read_tag_metadata_and_values_async(
        self,
    ) -> Tuple[List[tbase.TagData], List[Optional[SerializedTagWithAggregates]]]:
        def fn(token: str) -> Awaitable[Tuple[Any, HttpResponse]]:
            return self._api.as_async.get(
                "/{id}/tags-with-values", params={"id": token}
            )

        response, http_response = await self._ensure_selection_and_call_async(fn)
        return self._handle_read_tags_metadata_and_values(response, http_response)

    def _handle_read_tags_metadata_and_values(
        self, response: Any, http_response: HttpResponse
    ) -> Tuple[List[tbase.TagData], List[Optional[SerializedTagWithAggregates]]]:
        if (
            response is None
            or response.get("tagsWithValues") is None
            or any(
                t is None or t.get("tag") is None for t in response["tagsWithValues"]
            )
        ):
            raise tbase.TagManager.invalid_response(http_response)

        return (
            self._handle_read_tags_metadata(
                [t["tag"] for t in response["tagsWithValues"]], http_response
            ),
            self._handle_read_tags_values(
                response["tagsWithValues"],
                http_response,
                [t["tag"]["path"] for t in response["tagsWithValues"]],
            ),
        )

    def _reset_aggregates_internal(self) -> None:
        def fn(token: str) -> None:
            self._api.post("/{id}/reset-aggregates", params={"id": token})

        self._ensure_selection_and_call(fn)

    async def _reset_aggregates_internal_async(self) -> None:
        def fn(token: str) -> Awaitable[Tuple[None, HttpResponse]]:
            return self._api.as_async.post(
                "/{id}/reset-aggregates", params={"id": token}
            )

        await self._ensure_selection_and_call_async(fn)

    def _create_selection_on_server(self) -> None:
        selection, http_response = self._api.post(
            "", data={"searchPaths": list(self.paths)}
        )

        if selection is None or selection.get("id") is None:
            raise tbase.TagManager.invalid_response(http_response)

        self._token = selection["id"]
        self._selection_stale = False

    async def _create_selection_on_server_async(self) -> None:
        selection, http_response = await self._api.as_async.post(
            "", data={"searchPaths": list(self.paths)}
        )

        if selection is None or selection.get("id") is None:
            raise tbase.TagManager.invalid_response(http_response)

        self._token = selection["id"]
        self._selection_stale = False

    def _update_selection_on_server_if_needed(self) -> None:
        if self._selection_stale:
            self._api.put(
                "/{id}",
                data={"searchPaths": list(self.paths), "id": self._token},
                params={"id": self._token},
            )
            self._selection_stale = False

    async def _update_selection_on_server_if_needed_async(self) -> None:
        if self._selection_stale:
            await self._api.as_async.put(
                "/{id}",
                data={"searchPaths": list(self.paths), "id": self._token},
                params={"id": self._token},
            )
            self._selection_stale = False

    def _ensure_selection_and_call(self, api_call: Callable[[str], T]) -> T:
        if self._token is not None:
            try:
                self._update_selection_on_server_if_needed()
                return api_call(self._token)
            except core.ApiException as ex:
                if ex.http_status_code == 404:
                    # The server must have deleted it for inactivity. Recreate it below.
                    self._token = None
                else:
                    raise

        self._create_selection_on_server()
        assert self._token is not None
        return api_call(self._token)

    async def _ensure_selection_and_call_async(
        self, api_call: Callable[[str], Awaitable[T]]
    ) -> T:
        if self._token is not None:
            try:
                await self._update_selection_on_server_if_needed_async()
                return await api_call(self._token)
            except core.ApiException as ex:
                if ex.http_status_code == 404:
                    # The server must have deleted it for inactivity. Recreate it below.
                    self._token = None
                else:
                    raise

        await self._create_selection_on_server_async()
        assert self._token is not None
        return await api_call(self._token)
