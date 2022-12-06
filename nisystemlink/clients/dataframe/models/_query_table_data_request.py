from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._query_table_data_base import QueryTableDataBase


class ColumnOrderBy(JsonModel):
    """Specifies a column to order by and the ordering direction."""

    column: str
    """The name of the column to order by."""

    descending: Optional[bool] = None
    """Whether the ordering should be in descending order."""


class QueryTableDataRequest(QueryTableDataBase, WithPaging):
    """Contains the filtering and sorting options to use when querying table data."""

    order_by: Optional[List[ColumnOrderBy]] = None
    """A list of columns to order the results by. Multiple columns may be
    specified to order rows that have the same value for prior columns. The
    columns used for sorting do not need to be included in the columns list, in
    which case they are not returned. If ``order_by`` is not specified, then the
    order in which results are returned is undefined."""

    take: Optional[int] = None
    """Limits the returned list to the specified number of results."""
