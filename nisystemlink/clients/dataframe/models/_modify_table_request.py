from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ColumnMetadataPatch(JsonModel):
    """Specifies column properties to add, modify, or delete when editing table metadata."""

    name: str
    """The name of the column to modify."""

    properties: Dict[str, str | None]
    """The properties to modify. A map of key value properties containing the metadata
    to be added or modified. Set a property value to ``None`` to delete the property."""


class ModifyTableRequest(JsonModel):
    """Contains the metadata properties to modify. Values not included will remain unchanged."""

    metadata_revision: int | None = None
    """When specified, this is an integer that must match the last known
    revision number of the table, incremented by one. If it doesn't match the
    current ``metadataRevision`` incremented by one at the time of execution, the
    modify request will be rejected with a 409 Conflict. This is used to ensure
    that changes to this table's metadata are based on a known, previous
    state."""

    name: str | None = None
    """The new name of the table. Set to ``None`` to reset the name to the table's ID."""

    test_result_id: str | None = None
    """The new test result ID associated with the table. Set to ``None`` or an empty string to
    remove the test result ID. Added in version 2 of the
    :py:attr:`nisystemlink.clients.dataframe.models.OperationsV1.modify_metadata` operation. Older
    versions of the service will ignore this value."""

    workspace: str | None = None
    """The new workspace for the table. Set to ``None`` to reset to the
    default workspace. Changing the workspace requires permission to delete the
    table in its current workspace and permission to create the table in its new
    workspace."""

    properties: Dict[str, str | None] | None = None
    """The properties to modify. A map of key value properties containing the
    metadata to be added or modified. Set a property value to ``None`` to
    delete the property."""

    columns: List[ColumnMetadataPatch] | None = None
    """Updates to the column properties. Cannot add or remove columns, or change the name of a column."""
