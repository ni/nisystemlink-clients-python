from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._column import Column


class TableMetadata(JsonModel):
    """Contains information about a table, including its properties and column definitions."""

    columns: List[Column]
    """The list of columns in the table."""

    created_at: datetime
    """The date and time the table was created."""

    id: str
    """The table's unique identifier."""

    metadata_modified_at: datetime
    """The date and time the table's metadata was last modified."""

    metadata_revision: int
    """The table's metadata revision number, incremented each time the metadata is modified."""

    name: str
    """The name associated with the table."""

    properties: Dict[str, str]
    """User-defined properties associated with the table."""

    row_count: int
    """The number of rows in the table."""

    rows_modified_at: datetime
    """The date and time the table's data was last modified."""

    supports_append: bool
    """Whether the table supports appending additional rows of data."""

    workspace: str
    """The workspace the table belongs to."""
