from typing import Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class TableMetdataModificationBase(JsonModel):
    """Base class for table metadata modifications."""

    metadata_revision: Optional[int] = None
    """When specified, this is an integer that must match the last known
    revision number of the table, incremented by one. If it doesn't match the
    current ``metadataRevision`` incremented by one at the time of execution, the
    modify request will be rejected with a 409 Conflict. This is used to ensure
    that changes to this table's metadata are based on a known, previous
    state."""

    name: Optional[str] = None
    """The new name of the table. Setting to ``None`` will reset the name to the table's ID."""

    workspace: Optional[str] = None
    """The new workspace for the table. Setting to ``None`` will reset to the
    default workspace. Changing the workspace requires permission to delete the
    table in its current workspace and permission to create the table in its new
    workspace."""

    properties: Optional[Dict[str, Optional[str]]] = None
    """The properties to modify. A map of key value properties containing the
    metadata to be added or modified. Setting a property value to ``None`` will
    delete the property."""
