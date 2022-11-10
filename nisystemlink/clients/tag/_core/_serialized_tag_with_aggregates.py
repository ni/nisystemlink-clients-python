# -*- coding: utf-8 -*-

"""Implementation of SerializedTagWithAggregates."""

import datetime
from typing import Optional

from nisystemlink.clients import tag as tbase
from typing_extensions import final


@final
class SerializedTagWithAggregates:
    """Represents a generic tag value serialized to a string with optional aggregate
    values also serialized to a string.

    Clients typically do not interact with this instances of this class directly. Use a
    :class:`.TagValueReader` instead.
    """

    def __init_subclass__(cls) -> None:
        raise TypeError(
            "type 'SerializedTagWithAggregates' is not an acceptable base type"
        )

    def __init__(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
        count: Optional[int] = None,
        min: Optional[str] = None,
        max: Optional[str] = None,
        mean: Optional[float] = None,
    ) -> None:
        """Initialize an instance.

        Args:
            path: The path of the tag associated with the value.
            data_type: The data type of the value serialized as a string.
            value: The value serialized as a string.
            timestamp: The timestamp associated with the value.
            count: The number of times the tag has been written, or None if the tag is
                not collecting aggregates.
            min: The minimum value of the tag serialized to a string, or None if the tag
                is not collecting aggregates or the data type of the tag does not track
                a minimum value.
            max: The maximum value of the tag serialized to a string, or None if the tag
                is not collecting aggregates or the data type of the tag does not track
                a maximum value.
            mean: The mean value of the tag, or None if the tag is not collecting
                aggregates or the data type of the tag does not track a mean value.
        """
        self._path = path
        self._data_type = data_type
        self._value = value
        self._timestamp = timestamp
        self._count = count
        self._min = min
        self._max = max
        self._mean = mean

    @property
    def data_type(self) -> tbase.DataType:  # noqa: D401
        """The data type of the value that was serialized as a string."""
        return self._data_type

    @property
    def path(self) -> str:  # noqa: D401
        """The path of the tag associated with the value."""
        return self._path

    @property
    def value(self) -> str:  # noqa: D401
        """The value of the tag serialized as a string."""
        return self._value

    @property
    def timestamp(self) -> Optional[datetime.datetime]:  # noqa: D401
        """The timestamp associated with the value, if available."""
        return self._timestamp

    @property
    def count(self) -> Optional[int]:  # noqa: D401
        """The number of times the tag has been written, or None if the tag is not collecting aggregates."""
        return self._count

    @property
    def min(self) -> Optional[str]:  # noqa: D401
        """The minimum value of the tag serialized to a string, or None if the tag is
        not collecting aggregates or the data type of the tag does not track a minimum
        value.
        """
        return self._min

    @property
    def max(self) -> Optional[str]:  # noqa: D401
        """The maximum value of the tag serialized to a string, or None if the tag is
        not collecting aggregates or the data type of the tag does not track a maximum
        value.
        """
        return self._max

    @property
    def mean(self) -> Optional[float]:  # noqa: D401
        """The mean value of the tag, or None if the tag is not collecting aggregates or
        the data type of the tag does not track a mean value.
        """
        return self._mean
