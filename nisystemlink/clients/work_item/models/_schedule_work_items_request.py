from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._schedule_work_item_request import ScheduleWorkItemRequest


class ScheduleWorkItemsRequest(JsonModel):
    """Represents the request body content for scheduling multiple work items."""

    work_items: List[ScheduleWorkItemRequest]
    """List of work items to be scheduled."""

    replace: bool | None = None
    """If true, replaces existing scheduled work items."""
