from datetime import datetime
from typing import Any, Dict

from nisystemlink.clients.core._uplink._json_model import JsonModel


class NotebookMetadata(JsonModel):
    """Metadata for a notebook."""

    id: str | None = None
    """The ID of the notebook."""

    name: str | None = None
    """The name of the notebook."""

    workspace: str | None = None
    """The Id of the workspace containing the notebook."""

    created_by: str | None = None
    """The Id of the user that created the notebook."""

    updated_by: str | None = None
    """The Id of the user that last updated the notebook."""

    created_at: datetime | None = None
    """The created timestamp (ISO8601 format)."""

    updated_at: datetime | None = None
    """The last updated timestamp (ISO8601 format)."""

    properties: Dict[str, str] | None = None
    """A map of key value properties associated with the notebook."""

    metadata: Dict[str, Any] | None = None
    """The metadata of the notebook."""

    parameters: Dict[str, Any] | None = None
    """The parameters of the notebook."""
