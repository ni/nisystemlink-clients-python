from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._column_filter import ColumnFilter


class QueryTableDataBase(JsonModel):
    """Contains the common set of options when querying table data."""

    columns: List[str] | None = None
    """The names of columns to include in the response. The response will
    include the columns in the same order specified in this parameter. All
    columns are included in the order specified at table creation if this
    property is excluded."""

    filters: List[ColumnFilter] | None = None
    """A list of columns to filter by. Only rows whose columns contain values
    matching all of the specified filters are returned. The columns used for
    filtering do not need to be included in the columns list. When reading
    decimated data, the filters are applied before decimation."""
