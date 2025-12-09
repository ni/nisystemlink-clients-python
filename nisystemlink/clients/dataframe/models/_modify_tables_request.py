from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class TableMetadataModification(JsonModel):
    """Contains the metadata properties to modify. Values not included in the
    request or included with a ``None`` value will remain unchanged.
    """

    id: str
    """The ID of the table to modify."""

    metadata_revision: int | None = None
    """When specified, this is an integer that must match the last known
    revision number of the table, incremented by one. If it doesn't match the
    current ``metadataRevision`` incremented by one at the time of execution, the
    modify request will be rejected with a conflict error. This is used to
    ensure that changes to this table's metadata are based on a known, previous
    state."""

    name: str | None = None
    """The new name of the table."""

    test_result_id: str | None = None
    """The new test result ID associated with the table. Set to an empty string to remove
    the test result ID. Added in version 2 of the
    :py:attr:`nisystemlink.clients.dataframe.models.OperationsV1.modify_metadata` operation. Older
    versions of the service will ignore this value."""

    workspace: str | None = None
    """The new workspace for the table. Changing the workspace requires
    permission to delete the table in its current workspace and permission to
    create the table in its new workspace."""

    properties: Dict[str, str | None] | None = None
    """The properties to modify. A map of key value properties containing the
    metadata to be added or modified. Setting a property value to ``None`` will
    delete the property. Existing properties not included in the map are
    unaffected unless replace is true in the top-level request object."""


class ModifyTablesRequest(JsonModel):
    """Contains one or more table modifications to apply."""

    tables: List[TableMetadataModification]
    """The table modifications to apply. Each table may only appear once in the list."""

    replace: bool | None = None
    """When true, existing properties are replaced instead of merged."""
