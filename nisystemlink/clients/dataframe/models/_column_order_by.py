from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ColumnOrderBy(JsonModel):
    """Specifies a column to order by and the ordering direction."""

    column: str
    """The name of the column to order by."""

    descending: Optional[bool] = None
    """Whether the ordering should be in descending order."""
