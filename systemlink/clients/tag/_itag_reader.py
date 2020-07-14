# -*- coding: utf-8 -*-

"""Implementation of ITagReader."""

import abc
import datetime
import typing
from typing import Any, Callable, Optional

from systemlink.clients import core, tag as tbase
from systemlink.clients.core._internal._timestamp_utilities import TimestampUtilities
from systemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)
from typing_extensions import Literal


_DESERIALIZERS = {
    tbase.DataType.BOOLEAN: {"True": True, "False": False}.get,
    tbase.DataType.DATE_TIME: TimestampUtilities.str_to_datetime,
    tbase.DataType.DOUBLE: float,
    tbase.DataType.INT32: int,
    tbase.DataType.UINT64: int,
    tbase.DataType.STRING: str,
}


class _ITagReaderOverloads(abc.ABC):
    """Contains the overloaded methods of ITagReader.

    These overloads exist so that ``mypy`` can validate proper data types are used when
    reading tag values, as long as a literal DataType enum value is given when calling
    :meth:`get_tag_reader`. But they are hidden away in a base class so that they aren't
    documented by Sphinx, because Sphinx doesn't properly recognize the type annotations
    of overloads. See also: https://github.com/sphinx-doc/sphinx/issues/7901
    """

    @typing.overload
    def get_tag_reader(
        self, path: str, data_type: Literal[tbase.DataType.BOOLEAN]
    ) -> "tbase.TagValueReader[bool]":
        pass

    @typing.overload
    def get_tag_reader(
        self, path: str, data_type: Literal[tbase.DataType.DATE_TIME]
    ) -> "tbase.TagValueReader[datetime.datetime]":
        pass

    @typing.overload
    def get_tag_reader(
        self, path: str, data_type: Literal[tbase.DataType.DOUBLE]
    ) -> "tbase.TagValueReader[float]":
        pass

    @typing.overload
    def get_tag_reader(
        self, path: str, data_type: Literal[tbase.DataType.INT32]
    ) -> "tbase.TagValueReader[int]":
        pass

    @typing.overload
    def get_tag_reader(
        self, path: str, data_type: Literal[tbase.DataType.UINT64]
    ) -> "tbase.TagValueReader[int]":
        pass

    @typing.overload
    def get_tag_reader(
        self, path: str, data_type: Literal[tbase.DataType.STRING]
    ) -> "tbase.TagValueReader[str]":
        pass

    @typing.overload
    def get_tag_reader(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueReader[Any]":
        pass

    def get_tag_reader(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueReader":
        """Get a :class:`TagValueReader` for this path.

        Args:
            path: The path of the tag to read.
            data_type: The data type of the tag to read.
        """
        return self._get_tag_reader(path, data_type)

    @abc.abstractmethod
    def _get_tag_reader(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueReader":
        """Get a :class:`TagValueReader` for this path.

        Args:
            path: The path of the tag to read.
            data_type: The data type of the value to read.
        """
        ...


class ITagReader(_ITagReaderOverloads):
    """Provides an interface for reading the current and aggregate values of a single SystemLink tag."""

    def read(
        self,
        path: str,
        *,
        include_timestamp: bool = False,
        include_aggregates: bool = False
    ) -> Optional[tbase.TagWithAggregates]:
        """Retrieve the current value of the tag with the given ``path`` from the server.

        Optionally retrieves the aggregate values as well. The tag must exist.

        Args:
            path: The path of the tag to read.
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value, and the timestamp and/or aggregate values if requested, or None
            if the tag exists but doesn't have a value.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` is None.
            ReferenceError: if the reader has been closed.
            ApiException: if the API call fails.
        """
        data = self._read(path, include_timestamp, include_aggregates)
        if data is None or data.value is None:
            return None

        value = self._deserialize_value(data.value, data.data_type)
        if value is None:
            # TODO: Error information
            raise core.ApiException()

        return tbase.TagWithAggregates(
            data.path,
            data.data_type,
            value,
            data.timestamp,
            data.count,
            self._deserialize_value(data.min, data.data_type),
            self._deserialize_value(data.max, data.data_type),
            data.mean,
        )

    async def read_async(
        self,
        path: str,
        *,
        include_timestamp: bool = False,
        include_aggregates: bool = False
    ) -> Optional[tbase.TagWithAggregates]:
        """Asynchronously retrieve the current value of the tag with the given ``path`` from the server.

        Optionally retrieves the aggregate values as well. The tag must exist.

        Args:
            path: The path of the tag to read.
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value, and the timestamp and/or aggregate values if requested, or None
            if the tag exists but doesn't have a value.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` is None.
            ReferenceError: if the reader has been closed.
            ApiException: if the API call fails.
        """
        data = await self._read_async(path, include_timestamp, include_aggregates)
        if data is None or data.value is None:
            return None

        value = self._deserialize_value(data.value, data.data_type)
        if value is None:
            # TODO: Error information
            raise core.ApiException()

        return tbase.TagWithAggregates(
            data.path,
            data.data_type,
            value,
            data.timestamp,
            data.count,
            self._deserialize_value(data.min, data.data_type),
            self._deserialize_value(data.max, data.data_type),
            data.mean,
        )

    @abc.abstractmethod
    def _read(
        self, path: str, include_timestamp: bool, include_aggregates: bool
    ) -> Optional[SerializedTagWithAggregates]:
        """Retrieve the current value of the tag with the given ``path`` from the server.

        Optionally retrieves the aggregate values as well. The tag must exist. Clients
        do not typically call this method directly. Use a :class:`.TagValueReader`
        instead.

        Args:
            path: The path of the tag to read.
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value serialized as a string, or None if the tag exists but doesn't have
            a value.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` is None.
            ReferenceError: if the reader has been closed.
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _read_async(
        self, path: str, include_timestamp: bool, include_aggregates: bool
    ) -> Optional[SerializedTagWithAggregates]:
        """Asynchronously retrieve the current value of the tag with the given ``path`` from the server.

        Optionally retrieves the aggregate values as well. The tag must exist. Clients
        do not typically call this method directly. Use a :class:`.TagValueReader`
        instead.

        Args:
            path: The path of the tag to read.
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value serialized as a string, or None if the tag exists but doesn't have
            a value.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` is None.
            ReferenceError: if the reader has been closed.
            ApiException: if the API call fails.
        """
        ...

    @classmethod
    def _deserialize_value(cls, value: Optional[str], data_type: tbase.DataType) -> Any:
        if value is None:
            return None
        try:
            deserializer = typing.cast(Callable[[str], Any], _DESERIALIZERS[data_type])
        except KeyError:
            raise ValueError("data_type is unknown")
        try:
            return deserializer(value)
        except ValueError:
            return None

    def _get_tag_reader(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueReader":
        """Get a :class:`TagValueReader` for this path.

        Args:
            path: The path of the tag to read.
            data_type: The data type of the value to read.
        """
        return tbase.TagValueReader(self, tbase.TagData(path, data_type))
