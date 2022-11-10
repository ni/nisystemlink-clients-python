# -*- coding: utf-8 -*-

"""Implementation of SerializedTagWithAggregatesReader."""

from typing import Optional

from nisystemlink.clients import tag as tbase
from nisystemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)
from typing_extensions import final


@final
class SerializedTagWithAggregatesReader(tbase.ITagReader):
    """Represents an :class:`.ITagReader` wrapping a single :class:`SerializedTagWithAggregates`."""

    def __init_subclass__(cls) -> None:
        raise TypeError(
            "type 'SerializedTagWithAggregatesReader' is not an acceptable base type"
        )

    def __init__(self, value: SerializedTagWithAggregates) -> None:
        """Initialize a reader instance for the given value.

        Args:
            value: The value to wrap in a reader.

        Raises:
            ValueError: if ``value`` is None.
        """
        if value is None:
            raise ValueError("value cannot be None")
        self._value = value

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
        """
        if self._value.path == path:
            return self._value
        else:
            return None

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
        """
        if self._value.path == path:
            return self._value
        else:
            return None
