from typing import Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class UpdateMetadataRequest(JsonModel):
    """The file's metadata and options for updating it."""

    replace_existing: bool
    """Determines whether the current list should be entirely replaced by the specified list
        or merged with the existing list."""

    expected_revision: Optional[int]
    """When specified, this is an integer that should be set to match the last known revision number of the metadata.
    If it doesn't match at the time of execution, the update request will be rejected.
    This is used to ensure that changes to this file metadata are correctly using the previous state."""

    properties: Dict[str, str]
    """The properties to set. A map of key value properties containing the metadata to be attached.

        Predefined:
            Name: This is an optional property for renaming the file. When specified, the file will be renamed."""

    workspace: Optional[str]
    """When specified, the workspace of the metadata will be updated to the new value."""
