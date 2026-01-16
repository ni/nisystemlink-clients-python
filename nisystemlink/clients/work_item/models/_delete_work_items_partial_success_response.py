from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteWorkItemsPartialSuccessResponse(JsonModel):
    """Response for deleting work items with partial success."""

    deleted_ids: List[str] | None = None
    """List of work item IDs that were successfully deleted."""

    failed_ids: List[str] | None = None
    """List of work item IDs that failed to delete."""

    error: ApiError | None = None
    """The error that occurred when deleting the work items."""
