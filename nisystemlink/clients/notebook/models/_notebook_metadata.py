from datetime import datetime
from typing import Any, Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class NotebookMetadata(JsonModel):
    """Metadata for a notebook."""

    id: Optional[str] = None
    """The ID of the notebook."""

    name: Optional[str] = None
    """The name of the notebook."""

    workspace: Optional[str] = None
    """The Id of the workspace containing the notebook."""

    created_by: Optional[str] = None
    """The Id of the user that created the notebook."""

    updated_by: Optional[str] = None
    """The Id of the user that last updated the notebook."""

    created_at: Optional[datetime] = None
    """The created timestamp (ISO8601 format)."""

    updated_at: Optional[datetime] = None
    """The last updated timestamp (ISO8601 format)."""

    properties: Optional[Dict[str, str]] = None
    """A map of key value properties associated with the notebook."""

    metadata: Optional[Dict[str, Any]] = None
    """The metadata of the notebook."""

    parameters: Optional[Dict[str, Any]] = None
    """The parameters of the notebook."""
