# -*- coding: utf-8 -*-

"""Implementation of TagWithAggregates."""

import datetime
import math
from typing import Generic, Optional, TypeVar, Union

from systemlink.clients import core, tag as tbase


_NUMERIC_TYPES = set(
    (tbase.DataType.DOUBLE, tbase.DataType.INT32, tbase.DataType.UINT64)
)

_Any = TypeVar("_Any")


class TagWithAggregates(Generic[_Any]):
    """Represents a generic tag value with optional timestamp and optional aggregate values."""

    def __init__(
        self,
        path: str,
        data_type: tbase.DataType,
        value: _Any,
        timestamp: Optional[datetime.datetime] = None,
        count: Optional[int] = None,
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        mean: Optional[float] = None,
    ) -> None:
        """Initialize an instance.

        Args:
            path: The path of the tag associated with the value.
            data_type: The data type of the value.
            value: The value.
            timestamp: The timestamp associated with the value.
            count: The number of times the tag has been written, or None if the tag is
                not collecting aggregates.
            min: The minimum value of the tag, or None if the tag is not collecting
                aggregates or the data type of the tag does not track a minimum value.
            max: The maximum value of the tag, or None if the tag is not collecting
                aggregates or the data type of the tag does not track a maximum value.
            mean: The mean value of the tag, or None if the tag is not collecting
                aggregates or the data type of the tag does not track a mean value.

        Raises:
            ApiException: if min, max, or mean is None when it shouldn't be or non-None
                when it should be

        :meta private:
        """
        if data_type in _NUMERIC_TYPES:
            if count is not None:
                if mean is None or min is None or max is None:
                    # TODO: Error information
                    raise core.ApiException()
            elif min is not None or max is not None or mean is not None:
                # TODO: Error information: only valid if count is set
                raise core.ApiException()
        else:
            if (
                min is not None
                or max is not None
                or (mean is not None and not math.isnan(mean))
            ):
                # TODO: Error information: not supported for non-numerics
                raise core.ApiException()

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
        """The data type of the value."""
        return self._data_type

    @property
    def path(self) -> str:  # noqa: D401
        """The path of the tag associated with the value."""
        return self._path

    @property
    def value(self) -> _Any:  # noqa: D401
        """The value of the tag."""
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
    def min(self) -> Optional[Union[int, float]]:  # noqa: D401
        """The minimum value of the tag, or None if the tag is not collecting aggregates
        or the data type of the tag does not track a minimum value.
        """
        return self._min

    @property
    def max(self) -> Optional[Union[int, float]]:  # noqa: D401
        """The maximum value of the tag, or None if the tag is not collecting aggregates
        or the data type of the tag does not track a maximum value.
        """
        return self._max

    @property
    def mean(self) -> Optional[float]:  # noqa: D401
        """The mean value of the tag, or None if the tag is not collecting aggregates or
        the data type of the tag does not track a mean value.
        """
        return self._mean
