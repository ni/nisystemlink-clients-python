from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class FilterOperation(str, Enum):
    """Represents the different operations that can be used in a filter."""

    Equals = "EQUALS"
    NotEquals = "NOT_EQUALS"
    LessThan = "LESS_THAN"
    LessThanEquals = "LESS_THAN_EQUALS"
    GreaterThan = "GREATER_THAN"
    GreaterThanEquals = "GREATER_THAN_EQUALS"
    Contains = "CONTAINS"
    NotContains = "NOT_CONTAINS"


class ColumnFilter(JsonModel):
    """A filter to apply to the table data."""

    column: str
    """The name of the column to use for filtering."""

    operation: FilterOperation
    """How to compare the column's value with the specified value.

    An error is returned if the column's data type does not support the specified operation:
    * String columns only support ``EQUALS``, ``NOT_EQUALS``, ``CONTAINS``, and ``NOT_CONTAINS``.
    * Non-string columns do not support ``CONTAINS`` or ``NOT_CONTAINS``.
    * When ``value`` is ``None``, the operation must be ``EQUALS`` or ``NOT_EQUALS``.
    * When ``value`` is ``NaN`` for a floating-point column, the operation must be ``NOT_EQUALS``.
    """

    value: Optional[str]
    """The comparison value to use for filtering. An error will be returned if
    the value cannot be converted to the column's data type."""


class QueryTableDataBase(JsonModel):
    """Contains the common set of options when querying table data."""

    columns: Optional[List[str]] = None
    """The names of columns to include in the response. The response will
    include the columns in the same order specified in this parameter. All
    columns are included in the order specified at table creation if this
    property is excluded."""

    filters: Optional[List[ColumnFilter]] = None
    """A list of columns to filter by. Only rows whose columns contain values
    matching all of the specified filters are returned. The columns used for
    filtering do not need to be included in the columns list. When reading
    decimated data, the filters are applied before decimation."""
