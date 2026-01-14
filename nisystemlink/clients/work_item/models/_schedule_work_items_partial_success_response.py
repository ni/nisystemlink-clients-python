from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._schedule_work_items_request import ScheduleWorkItemRequest
from ._work_item import WorkItem


class ScheduleWorkItemsPartialSuccessResponse(JsonModel):
    """Response for scheduling one or more work items."""

    scheduled_work_items: List[WorkItem] | None = None
    """List of successfully scheduled work items."""

    failed_work_items: List[ScheduleWorkItemRequest] | None = None
    """List of work item requests that failed to schedule."""

    error: ApiError | None = None
    """The error that occurred when scheduling the work items."""
