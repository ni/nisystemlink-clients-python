from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._query_table_data_base import QueryTableDataBase


class DecimationMethod(str, Enum):
    """Represents the different methods that can be used to decimate data."""

    Lossy = "LOSSY"
    """Creates an ``x_column`` ordered set and returns an uniformly distributed
    sample of rows with as many rows as the number specified as ``intervals.``"""

    MaxMin = "MAX_MIN"
    """Creates an ``x_column`` ordered set which will be divided in the number of
    ``intervals`` specified. For each of the intervals, the maximum and minimum
    values for all the columns specified in ``y_columns`` will be returned."""

    EntryExit = "ENTRY_EXIT"
    """Creates an ``x_column`` ordered set which will be divided in the number of
    ``intervals`` specified. For each of the intervals, the first and last row
    within the interval will be returned in addition to the maximum and minimum
    values for all the columns specified in ``y_columns``."""


class DecimationOptions(JsonModel):
    """Contains the parameters to use for data decimation."""

    x_column: Optional[str] = None
    """The name of the column that will be used as the x-axis for decimating the
    data. The column in the table that was specified as Index will be used if
    this field is excluded. Only numeric columns are supported. i.e. ``INT32``,
    ``INT64``, ``FLOAT32``, ``FLOAT64`` and ``TIMESTAMP``."""

    y_columns: Optional[List[str]] = None
    """A list of columns to decimate by. This property is only needed when the
    specified method is ``MAX_MIN`` or ``ENTRY_EXIT``. Only numeric columns are
    supported. i.e. ``INT32``, ``INT64``, ``FLOAT32``, ``FLOAT64`` and
    ``TIMESTAMP``."""

    intervals: Optional[int] = None
    """Number of intervals to use for decimation. Defaults to 1000."""

    method: Optional[DecimationMethod] = None
    """Specifies the method used to decimate the data. Defaults to
    :class:`DecimationMethod.Lossy`"""


class QueryDecimatedDataRequest(QueryTableDataBase):
    """Specifies the columns, filters and decimation parameters for a query."""

    decimation: Optional[DecimationOptions] = None
    """The decimation options to use when querying data. If not specified, the
    default is to use :class:`DecimationMethod.Lossy` with 1000 intervals over
    the table's index column."""
