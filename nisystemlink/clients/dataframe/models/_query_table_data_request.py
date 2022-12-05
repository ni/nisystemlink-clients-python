from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.core._uplink._with_paging import WithPaging


class ColumnOrderBy(JsonModel):
    """Specifies a column to order by and the ordering direction."""

    column: str
    """The name of the column to order by."""

    descending: Optional[bool] = None
    """Whether the ordering should be in descending order."""


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


class QueryTableDataRequest(WithPaging):
    """Contains the filtering and sorting options to use when querying table data."""

    columns: Optional[List[str]] = None
    """The names of columns to include in the response. The response will
    include the columns in the same order specified in this parameter. All
    columns are included in the order specified at table creation if this
    property is excluded."""

    order_by: Optional[List[ColumnOrderBy]] = None
    """A list of columns to order the results by. Multiple columns may be
    specified to order rows that have the same value for prior columns. The
    columns used for sorting do not need to be included in the columns list, in
    which case they are not returned. If ``order_by`` is not specified, then the
    order in which results are returned is undefined."""

    filters: Optional[List[ColumnFilter]] = None
    """A list of columns to filter by. Only rows whose columns contain values
    matching all of the specified filters are returned. The columns used for
    filtering do not need to be included in the columns list."""

    take: Optional[int] = None
    """Limits the returned list to the specified number of results."""
