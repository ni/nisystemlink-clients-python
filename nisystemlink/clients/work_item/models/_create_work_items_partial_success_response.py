from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._create_work_item_request import CreateWorkItemRequest
from ._work_item import WorkItem


class CreateWorkItemsPartialSuccessResponse(JsonModel):
    """Response for creating work items with partial success."""

    created_work_items: List[WorkItem]
    """List of successfully created work items."""

    failed_work_items: List[CreateWorkItemRequest] | None = None
    """List of work item requests that failed during creation."""

    error: ApiError | None = None
    """The error that occurred when creating the work items."""
