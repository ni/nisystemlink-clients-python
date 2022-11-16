from typing import Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._column_type import ColumnType
from ._data_type import DataType


class Column(JsonModel):
    """Defines a single column in a table."""

    name: str
    """The column name, which must be unique across all columns in the table."""

    data_type: DataType
    """The data type of the column."""

    column_type: ColumnType = ColumnType.Normal
    """The column type. Defaults to ColumnType.Normal."""

    properties: Optional[Dict[str, str]] = None
    """User-defined properties associated with the column."""
