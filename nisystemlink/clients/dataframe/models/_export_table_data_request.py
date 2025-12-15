from enum import Enum
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._column_filter import ColumnFilter
from ._column_order_by import ColumnOrderBy


class ExportFormat(str, Enum):
    """The format of the exported data."""

    CSV = "CSV"
    """Comma-separated values."""


class ExportTableDataRequest(JsonModel):
    """Specifies the parameters for a data export with ordering and filtering."""

    columns: List[str] | None = None
    """The names of columns to include in the export. The export will
    include the columns in the same order specified in this parameter. All
    columns are included in the order specified at table creation if this
    property is excluded."""

    order_by: List[ColumnOrderBy] | None = None
    """A list of columns to order the results by. Multiple columns may be
    specified to order rows that have the same value for prior columns. The
    columns used for sorting do not need to be included in the columns list, in
    which case they are not included in the export."""

    filters: List[ColumnFilter] | None = None
    """A list of columns to filter by. Only rows whose columns contain values
    matching all of the specified filters are returned. The columns used for
    filtering do not need to be included in the columns list, in which case
    they are not included in the export."""

    take: int | None = None
    """The maximum number of rows to include in the export. If ``None``
    (the default), all rows are included. Added in version 3 of the
    :py:attr:`nisystemlink.clients.dataframe.models.OperationsV1.read_data`
    operation. Older versions of the service will ignore this value and
    always include all rows."""

    response_format: ExportFormat
    """The format of the exported data. The only response format
    currently supported is ``CSV``."""
