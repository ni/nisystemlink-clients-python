from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class TableMetdataModification(JsonModel):
    """Contains the metadata properties to modify. Values not included in the
    request or included with a ``None`` value will remain unchanged.
    """

    id: str
    """The ID of the table to modify."""

    metadata_revision: Optional[int] = None
    """When specified, this is an integer that must match the last known
    revision number of the table, incremented by one. If it doesn't match the
    current ``metadataRevision`` incremented by one at the time of execution, the
    modify request will be rejected with a conflict error. This is used to
    ensure that changes to this table's metadata are based on a known, previous
    state."""

    name: Optional[str] = None
    """The new name of the table."""

    workspace: Optional[str] = None
    """The new workspace for the table. Changing the workspace requires
    permission to delete the table in its current workspace and permission to
    create the table in its new workspace."""

    properties: Optional[Dict[str, Optional[str]]] = None
    """The properties to modify. A map of key value properties containing the
    metadata to be added or modified. Setting a property value to ``None`` will
    delete the property. Existing properties not included in the map are
    unaffected unless replace is true in the top-level request object."""


class ModifyTablesRequest(JsonModel):
    """Contains one or more table modifications to apply."""

    tables: List[TableMetdataModification]
    """The table modifications to apply. Each table may only appear once in the list."""

    replace: Optional[bool] = None
    """When true, existing properties are replaced instead of merged."""
