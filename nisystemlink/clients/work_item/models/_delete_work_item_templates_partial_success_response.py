from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteWorkItemTemplatesPartialSuccessResponse(JsonModel):
    """Response for deleting work item templates with partial success."""

    deleted_ids: List[str] | None = None
    """List of work item template IDs that were successfully deleted."""

    failed_ids: List[str] | None = None
    """List of work item template IDs that failed to delete."""

    error: dict | None = None
    """Error information if any failures occurred."""
