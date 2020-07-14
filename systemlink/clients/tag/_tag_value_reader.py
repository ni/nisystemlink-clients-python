# -*- coding: utf-8 -*-

"""Implementation of TagValueReader."""

from typing import Generic, Optional, TypeVar

from systemlink.clients import core, tag as tbase

_Any = TypeVar("_Any")


class TagValueReader(Generic[_Any]):
    """Represents the ability to read a single tag's value using an :class:`ITagReader`."""

    def __init__(self, reader: tbase.ITagReader, tag: tbase.TagData) -> None:
        """Initialize an instance.

        Args:
            reader: The :class:`ITagReader` to use when reading values.
            tag: The tag whose values will be read.
            path: The path of the tag whose values will be read.

        Raises:
            ValueError: if ``tag`` is not a tag of a valid data type and with a valid
                path.
        """
        if tag.data_type == tbase.DataType.UNKNOWN:
            raise ValueError("tag.data_type cannot be UNKNOWN")

        self._path = tag.validate_path()
        self._data_type = tag.data_type
        self.__reader = reader

    @property
    def data_type(self) -> tbase.DataType:  # noqa: D401
        """The data type of the tag associated with the value."""
        return self._data_type

    @property
    def path(self) -> str:  # noqa: D401
        """The path of the tag associated with the value."""
        return self._path

    @property
    def _reader(self) -> tbase.ITagReader:  # noqa: D401
        """The underlying :class:`ITagReader` for reading values."""
        return self.__reader

    def read(
        self, *, include_timestamp: bool = False, include_aggregates: bool = False
    ) -> Optional[tbase.TagWithAggregates[_Any]]:
        """Read the current value of the tag.

        Args:
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value, and the timestamp and/or aggregate values if requested, or None
            if the tag exists but doesn't have a value.

        Raises:
            ReferenceError: if the underlying reader has been closed.
            ApiException: if the API call fails.
        """
        ret = self._reader.read(
            self._path,
            include_timestamp=include_timestamp,
            include_aggregates=include_aggregates,
        )
        if ret is None:
            return None
        if ret.data_type != self.data_type:
            raise core.ApiException("Tag data type does not match")

        return ret

    async def read_async(
        self, *, include_timestamp: bool = False, include_aggregates: bool = False
    ) -> Optional[tbase.TagWithAggregates[_Any]]:
        """Read the current value of the tag.

        Args:
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value, and the timestamp and/or aggregate values if requested, or None
            if the tag exists but doesn't have a value.

        Raises:
            ReferenceError: if the underlying reader has been closed.
            ApiException: if the API call fails.
        """
        ret = await self._reader.read_async(
            self._path,
            include_timestamp=include_timestamp,
            include_aggregates=include_aggregates,
        )
        if ret is None:
            return None
        if ret.data_type != self.data_type:
            raise core.ApiException("Tag data type does not match")

        return ret
