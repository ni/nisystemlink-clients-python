from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._update_work_item_request import UpdateWorkItemRequest


class UpdateWorkItemsRequest(JsonModel):
    """Represents the request body content for updating multiple work items."""

    work_items: List[UpdateWorkItemRequest]
    """List of work items to update."""

    replace: bool | None = None
    """When true, existing array and key-value pair fields are replaced instead of merged."""
