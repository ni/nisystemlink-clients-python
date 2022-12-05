from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._data_frame import DataFrame


class PagedTableRows(WithPaging):
    """Contains the result of a query for rows of data."""

    frame: DataFrame
    """The data frame containing the rows of data."""

    total_row_count: int
    """The total number of rows matched by the query across all pages of results."""
