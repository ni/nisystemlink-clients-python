from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._column_filter import ColumnFilter
from ._column_order_by import ColumnOrderBy


class ExportFormat(str, Enum):
    """The format of the exported data."""

    CSV = "CSV"
    """Comma-separated values."""


class ExportTableDataRequest(JsonModel):
    """Specifies the parameters for a data export with ordering and filtering."""

    columns: Optional[List[str]] = None
    """The names of columns to include in the export. The export will
    include the columns in the same order specified in this parameter. All
    columns are included in the order specified at table creation if this
    property is excluded."""

    order_by: Optional[List[ColumnOrderBy]] = None
    """A list of columns to order the results by. Multiple columns may be
    specified to order rows that have the same value for prior columns. The
    columns used for sorting do not need to be included in the columns list, in
    which case they are not included in the export."""

    filters: Optional[List[ColumnFilter]] = None
    """A list of columns to filter by. Only rows whose columns contain values
    matching all of the specified filters are returned. The columns used for
    filtering do not need to be included in the columns list, in which case
    they are not included in the export."""

    response_format: ExportFormat
    """The format of the exported data. The only response format
    currently supported is ``CSV``."""
