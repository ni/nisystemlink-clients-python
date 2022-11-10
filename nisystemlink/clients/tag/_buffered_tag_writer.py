# -*- coding: utf-8 -*-

"""Implementation of BufferedTagWriter."""

import abc
import datetime
import sys
import threading
from types import TracebackType
from typing import Any, Callable, Optional, Type

from nisystemlink.clients import core, tag as tbase
from nisystemlink.clients.tag._core._itime_stamper import ITimeStamper
from nisystemlink.clients.tag._core._manual_reset_timer import ManualResetTimer


class BufferedTagWriter(tbase.ITagWriter):
    """Represents an :class:`ITagWriter` that buffers tag writes instead of sending them immediately.

    Writes that utilize automatic timestamps are based on the system time when buffered.
    Implementations may provide automatic sending of buffered writes based on different
    conditions. Unsent writes are discarded when the instance is deleted.

    Note that :class:`BufferedTagWriter` objects support using the ``with`` statement
    (or the ``async with`` statement), to automatically :meth:`send
    <send_buffered_writes>` any remaining buffered writes on exit.
    """

    def __init__(
        self, stamper: ITimeStamper, buffer_size: int, flush_timer: ManualResetTimer
    ) -> None:
        """Initialize the writer.

        Args:
            stamper: An object for time-stamping tag writes.
            buffer_size: The maximum number of tag writes to buffer before automatically
                sending them to the server.
            flush_timer: A timer that, once started, elapses whenever buffered writes
                should be sent automatically. Does not have to be a configured timer.
        """
        self._lock = threading.Lock()
        self._buffer_limit = buffer_size
        self._flush_timer = flush_timer
        self._stamper = stamper

        self._closed = False
        self._num_buffered = 0
        self._send_error = None  # type: Optional[core.ApiException]
        self._timer_generation = 0
        self._timer_handler = None  # type: Optional[Callable[[], None]]

    @abc.abstractmethod
    def _buffer_value(self, path: str, value: Any) -> None:
        """Add a value to the buffer.

        Args:
            path: The tag path being written.
            value: The value being written.
        """
        ...

    @abc.abstractmethod
    def _clear_buffer(self) -> None:
        """Clear the buffer of writes."""
        ...

    @abc.abstractmethod
    def _copy_buffer(self) -> Any:
        """Return the contents of the buffer and clears or replaces the buffer used for future writes.

        Returns:
            The buffered data.
        """
        ...

    @abc.abstractmethod
    def _create_item(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> Any:
        """Return an item that can be placed into the buffer.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the value to write.
            value: The tag value to write, serialized as a string.
            timestamp: The timestamp represented as a nullable ``datetime.datetime``.

        Returns:
            The created item.

        Raises:
            ValueError: if ``data_type`` is not supported for writing.
        """
        ...

    @abc.abstractmethod
    def _send_writes(self, updates: Any) -> None:
        """Send the writes stored in ``updates`` to the server.

        Args:
            updates: The writes to send.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _send_writes_async(self, updates: Any) -> None:
        """Asynchronously send the writes stored in ``updates`` to the server.

        Args:
            updates: The writes to send.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    def clear_buffered_writes(self) -> None:
        """Clear any pending writes from :meth:`write()`.

        Raises:
            ReferenceError: if the writer has been closed.
        """
        if self._closed:
            raise ReferenceError("BufferedTagWriter")

        with self._lock:
            self._stop_timer_while_locked()
            self._clear_buffer()
            self._num_buffered = 0

    def send_buffered_writes(self) -> None:
        """Write all of the pending writes from :meth:`write()` to the server.

        Does nothing if there are no pending writes.

        Raises:
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("BufferedTagWriter")

        with self._lock:
            updates = self._retrieve_buffered_values_while_locked()

        if updates is not None:
            self._send_writes(updates)

    async def send_buffered_writes_async(self) -> None:
        """Asynchronously write all of the pending writes from :meth:`write()` to the server.

        Does nothing if there are no pending writes.

        Raises:
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("BufferedTagWriter")

        with self._lock:
            updates = self._retrieve_buffered_values_while_locked()

        if updates is not None:
            await self._send_writes_async(updates)

    def __enter__(self) -> "BufferedTagWriter":
        if self._closed:
            raise ReferenceError("BufferedTagWriter")

        self._flush_timer.__enter__()
        return self

    async def __aenter__(self) -> "BufferedTagWriter":
        if self._closed:
            raise ReferenceError("BufferedTagWriter")

        await self._flush_timer.__aenter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if self._closed:
            return False

        self.send_buffered_writes()
        self._closed = True

        suppress = self._flush_timer.__exit__(exc_type, exc_val, exc_tb)
        return suppress

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if self._closed:
            return False

        await self.send_buffered_writes_async()
        self._closed = True

        suppress = await self._flush_timer.__aexit__(exc_type, exc_val, exc_tb)
        return suppress

    def _write(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None:
        """Write a tag's value that's been serialized to a string.

        Clients do not typically call this method directly. Use a
        :class:`.TagValueWriter` instead.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the value to write.
            value: The tag value to write, serialized as a string.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Raises:
            ValueError: if `path` is empty or invalid.
            ValueError: if `path` or `value` is None.
            ValueError: if `data_type` is invalid.
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        timestamped_value = self._prepare_write(path, data_type, value, timestamp)

        pending_error = None
        updates = None
        with self._lock:
            self._buffer_value(path, timestamped_value)
            self._num_buffered += 1

            if self._num_buffered == self._buffer_limit:
                updates = self._retrieve_buffered_values_while_locked()
            elif self._num_buffered == 1:
                self._start_timer_while_locked()

            if self._send_error is not None:
                pending_error = self._send_error
                self._send_error = None

        if updates is not None:
            self._send_writes(updates)

        if pending_error:
            raise pending_error

    async def _write_async(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None:
        """Asynchronously write a tag's value that's been serialized to a string.

        Clients do not typically call this method directly. Use a
        :class:`.TagValueWriter` instead.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the value to write.
            value: The tag value to write, serialized as a string.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ValueError: if `path` is empty or invalid.
            ValueError: if `path` or `value` is None.
            ValueError: if `data_type` is invalid.
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        timestamped_value = self._prepare_write(path, data_type, value, timestamp)

        pending_error = None
        updates = None
        with self._lock:
            self._buffer_value(path, timestamped_value)
            self._num_buffered += 1

            if self._num_buffered == self._buffer_limit:
                updates = self._retrieve_buffered_values_while_locked()
            elif self._num_buffered == 1:
                self._start_timer_while_locked()

            if self._send_error is not None:
                pending_error = self._send_error
                self._send_error = None

        if updates is not None:
            await self._send_writes_async(updates)

        if pending_error:
            raise pending_error

    def _prepare_write(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> Any:
        if self._closed:
            raise ReferenceError("BufferedTagWriter")

        if value is None:
            raise ValueError("value is None")

        if data_type == tbase.DataType.UNKNOWN:
            raise ValueError("data_type is UNKNOWN")

        if timestamp is None:
            timestamp = self._stamper.timestamp
        else:
            if timestamp.tzinfo is None and sys.version_info < (3, 6):
                # python 3.5's .astimezone fails if given a naive datetime, so use a
                # roundabout method; python 3.6+ allow naive datetimes and assume a
                # local timezone, so allow the same here
                timestamp = datetime.datetime.fromtimestamp(
                    timestamp.timestamp(), datetime.timezone.utc
                )
            else:
                timestamp = timestamp.astimezone(datetime.timezone.utc)
        return self._create_item(
            tbase.TagPathUtilities.validate(path), data_type, value, timestamp
        )

    def _retrieve_buffered_values_while_locked(self) -> Any:
        """Return the buffered values, if any, and clears the buffer.

        Must hold :attr:`_lock`.

        Returns:
            The buffered values, or None if there aren't any.
        """
        self._stop_timer_while_locked()

        if self._num_buffered == 0:
            return None

        buffer = self._copy_buffer()
        self._num_buffered = 0
        return buffer

    def _start_timer_while_locked(self) -> None:
        """Start the flush timer, if configured.

        Must hold :attr:`_lock`.
        """
        if not self._flush_timer.can_start:
            return

        handler_generation = self._timer_generation
        self._flush_timer.elapsed -= self._timer_handler
        self._timer_handler = lambda: self._timer_expired(handler_generation)
        self._flush_timer.elapsed += self._timer_handler
        self._flush_timer.start()

    def _stop_timer_while_locked(self) -> None:
        """Stop the flush timer, if configured.

        Must hold :attr:`_lock`.
        """
        self._flush_timer.stop()
        self._timer_generation += 1

    def _timer_expired(self, generation: int) -> None:
        if self._closed:
            return

        with self._lock:
            if generation != self._timer_generation:
                # The timer was canceled after we were already queued.
                return

            updates = self._retrieve_buffered_values_while_locked()

        if updates is not None:
            try:
                self._send_writes(updates)
            except core.ApiException as ex:
                with self._lock:
                    self._send_error = ex
