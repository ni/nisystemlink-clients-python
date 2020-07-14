# -*- coding: utf-8 -*-

"""Implementation of TagSubscription."""

import abc
import contextlib
import datetime
import weakref
from types import TracebackType
from typing import Iterable, List, Optional, Type

import events
from systemlink.clients import core, tag as tbase
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer


class TagSubscription(events.Events, abc.ABC):
    """Represents a subscription for changes to one or more tags' values.

    Call :meth:`close()` to stop receiving events.

    Note that :class:`TagSubscription` objects support using the ``with`` statement (or
    the ``async with`` statement), to :meth:`close()` the subsription automatically on
    exit.

    Attributes:
        tag_changed: An event that is triggered when one of the subscription's tag
            changes. The callback will receive a :class:`TagData` parameter and an
            :class:`Optional` [:class:`TagValueReader`] parameter.

            Example::

                def my_callback(tag: TagData, reader: Optional[TagValueReader]):
                    print("{} changed".format(tag.path))
                    if reader is None:
                        print(" - unknown data type")
                    else:
                        value = reader.read()
                        assert value is not None
                        print(" - new value: {}".format(value.value))

                subscription.tag_changed += my_callback
    """

    __events__ = ["tag_changed"]
    # Under certain circumstances, mypy complains about the event not having a type hint
    # unless we specify it explicitly. (But we also need to delete the attribute so that
    # Events.__getattr__ can do its magic.)
    tag_changed = None  # type: events._EventSlot
    del tag_changed

    _HEARTBEAT_INTERVAL_MILLISECONDS = 30000.0
    """Send a heartbeat every 30 seconds based on a server-side expiration of 60 seconds."""

    def __init__(
        self, paths: Iterable[str], heartbeat_timer: Optional[ManualResetTimer]
    ) -> None:
        """Initialize the instance.

        Derived types must call :meth:`_initialize()` or :meth:`_initialize_async()`
        after construction.

        Args:
            paths: The tag path queries to include in the subscription.
            heartbeat_timer: A timer for sending a heartbeat to keep the subscription
                alive for testing purposes, or None to use a default timer.

        Raises:
            ValueError: if ``paths`` is None.
        """
        if paths is None:
            raise ValueError("paths cannot be None")

        super().__init__()
        self._paths = list(paths)
        if heartbeat_timer is not None:
            self._heartbeat_timer = heartbeat_timer
        else:
            self._heartbeat_timer = ManualResetTimer(
                datetime.timedelta(milliseconds=self._HEARTBEAT_INTERVAL_MILLISECONDS)
            )
        self._exit_stack = contextlib.ExitStack()
        self._exit_stack.enter_context(self._heartbeat_timer)

        callback_ref = weakref.WeakMethod(self._heartbeat_timer_elapsed)  # type: ignore

        def callback() -> None:
            actual_callback = callback_ref()  # type: ignore
            if actual_callback:
                actual_callback()

        self._heartbeat_timer_handler = callback
        self._heartbeat_timer.elapsed += self._heartbeat_timer_handler
        self._closed = False

    def __del__(self) -> None:
        self._exit_stack.close()

    def _initialize(self) -> None:
        """Create and initialize the subscription.

        Derived types must call this method or :meth:`_initialize_async()` after
        construction to create and keep the subscription alive.

        Raises:
            ApiException: if the API call fails.
        """
        self._create_subscription_on_server(self._paths)
        self._heartbeat_timer.start()

    async def _initialize_async(self) -> None:
        """Asynchronously create and initializes the subscription.

        Derived types must call this method or :meth:`_initialize()` after construction
        to create and keep the subscription alive.

        Raises:
            ApiException: if the API call fails.
        """
        await self._create_subscription_on_server_async(self._paths)
        self._heartbeat_timer.start()

    @abc.abstractmethod
    def _create_subscription_on_server(self, paths: List[str]) -> None:
        """Create the subscription on the server.

        Implementations should retrieve and throw away the first set of updates before
        returning.

        Args:
            paths: The tag path queries to include in the subscription.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _create_subscription_on_server_async(self, paths: List[str]) -> None:
        """Asynchronously create the subscription on the server.

        Implementations should retrieve and throw away the first set of updates before
        returning.

        Args:
            paths: The tag path queries to include in the subscription.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    def _send_heartbeat(self) -> None:
        """Send a heartbeat for the subscription to keep it active.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    def _close_internal(self) -> None:
        """Clean up server resources associated with the subscription."""
        ...

    @abc.abstractmethod
    async def _close_internal_async(self) -> None:
        """Asynchronously clean up server resources associated with the subscription.

        Returns:
            A task representing the asynchronous operation.
        """
        ...

    def close(self) -> None:
        """Close server resources associated with the subscription.

        Further tag writes will not trigger new events.
        """
        if self._closed:
            return

        self._close_internal()
        self._heartbeat_timer.elapsed -= self._heartbeat_timer_handler
        self._closed = True

    async def close_async(self) -> None:
        """Asynchronously close server resources associated with the subscription.

        Further tag writes will not trigger new events.

        Returns:
            A task representing the asynchronous operation.
        """
        if self._closed:
            return

        await self._close_internal_async()
        self._heartbeat_timer.elapsed -= self._heartbeat_timer_handler
        self._closed = True

    def __enter__(self) -> "TagSubscription":
        return self

    async def __aenter__(self) -> "TagSubscription":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """Close server resources associated with the subscription.

        Further tag writes will not trigger new events.
        """
        suppress = False
        try:
            self.close()
        finally:
            suppress = self._exit_stack.__exit__(exc_type, exc_val, exc_tb)
        return suppress

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """Asynchronously close server resources associated with the subscription.

        Further tag writes will not trigger new events.
        """
        suppress = False
        try:
            await self.close_async()
        finally:
            suppress = self._exit_stack.__exit__(exc_type, exc_val, exc_tb)
        return suppress

    def _on_tag_changed(
        self, tag: tbase.TagData, value: Optional[tbase.TagValueReader]
    ) -> None:
        """Raise the :attr:`tag_changed` event.

        Args:
            tag: The tag that was changed.
            value: The new value and any associated information, or None if the tag has
                an unknown data type.
        """
        self.tag_changed(tag, value)

    def _heartbeat_timer_elapsed(self) -> None:
        try:
            self._send_heartbeat()
        except core.ApiException:
            try:
                self._create_subscription_on_server(self._paths)
            except core.ApiException:
                # Ignore, we'll try again later
                pass

        self._heartbeat_timer.start()
