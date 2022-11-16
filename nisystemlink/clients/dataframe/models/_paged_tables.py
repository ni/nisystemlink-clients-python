from typing import List

from nisystemlink.clients.core._uplink._paged_result import PagedResult

from ._table_metadata import TableMetadata


class PagedTables(PagedResult):
    """The response for a table query containing the matched tables."""

    tables: List[TableMetadata]
    """The list of tables returned by the query."""
