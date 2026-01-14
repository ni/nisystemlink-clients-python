from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._work_item import WorkItem
from ._update_work_item_request import UpdateWorkItemRequest


class UpdateWorkItemsPartialSuccessResponse(JsonModel):
    """Represents the response after attempting to update work items."""

    updated_work_items: List[WorkItem] | None = None
    """List of successfully updated work items."""

    failed_work_items: List[UpdateWorkItemRequest] | None = None
    """List of work items that failed to update."""

    error: ApiError | None = None
    """The error that occurred when updating the work items."""
