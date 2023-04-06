from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._column_order_by import ColumnOrderBy
from ._query_table_data_base import QueryTableDataBase


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
