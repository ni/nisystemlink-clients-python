from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._column import Column


class CreateTableRequest(JsonModel):
    """Contains information needed to create a table, including its properties and column definitions."""

    columns: List[Column]
    """The list of columns in the table. Exactly one column must have a :class:`.ColumnType` of INDEX."""

    name: str | None = None
    """The name to associate with the table. When not specified, a name will be
    assigned from the table's ID."""

    properties: Dict[str, str] | None = None
    """User-defined properties to associate with the table."""

    workspace: str | None = None
    """The workspace to create the table in. Uses the default workspace when not specified."""
