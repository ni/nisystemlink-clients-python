# -*- coding: utf-8 -*-

"""Implementation of TagValueWriter."""

import datetime
import typing
from typing import Any, Awaitable, Generic, Optional, TypeVar

from systemlink.clients import tag as tbase

_Any = TypeVar("_Any")


class TagValueWriter(Generic[_Any]):
    """Represents the ability to write a single tag's value using an :class:`ITagWriter`."""

    def __init__(self, writer: tbase.ITagWriter, tag: tbase.TagData) -> None:
        """Initialize an instance.

        Args:
            writer: The :class:`ITagWriter` to use when writing values.
            tag: The tag whose values will be written.
            path: The path of the tag whose values will be written.

        Raises:
            ValueError: if ``tag`` is not a tag of a valid type and with a valid path.
        """
        if tag.data_type == tbase.DataType.UNKNOWN:
            raise ValueError("tag.type cannot be UNKNOWN")

        self._path = tag.validate_path()
        self._data_type = tag.data_type
        self.__writer = writer

    @property
    def data_type(self) -> tbase.DataType:  # noqa: D401
        """The data type of the tag associated with the value."""
        return self._data_type

    @property
    def path(self) -> str:  # noqa: D401
        """The path of the tag associated with the value."""
        return self._path

    @property
    def _writer(self) -> tbase.ITagWriter:  # noqa: D401
        """The underlying :class:`ITagWriter` for writing values."""
        return self.__writer

    def write(
        self, value: _Any, *, timestamp: Optional[datetime.datetime] = None
    ) -> None:
        """Write the tag's value.

        Args:
            value: The tag value to write.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Raises:
            ReferenceError: if the underlying writer has been closed.
            ApiException: if the API call fails.
        """
        self._writer.write(
            self._path, self._data_type, typing.cast(Any, value), timestamp=timestamp
        )

    def write_async(
        self, value: _Any, *, timestamp: Optional[datetime.datetime] = None
    ) -> Awaitable[None]:
        """Write the tag's value.

        Args:
            value: The tag value to write.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Raises:
            ReferenceError: if the underlying writer has been closed.
            ApiException: if the API call fails.
        """
        return self._writer.write_async(
            self._path, self._data_type, typing.cast(Any, value), timestamp=timestamp
        )
