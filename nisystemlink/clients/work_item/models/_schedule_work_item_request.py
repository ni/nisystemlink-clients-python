from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._resources_definition import ScheduleResourcesDefinition
from ._schedule_definition import ScheduleDefinition


class ScheduleWorkItemRequest(JsonModel):
    """Represents the request body content for scheduling a single work item."""

    id: str
    """The ID of the work item to be scheduled."""

    assigned_to: str | None = None
    """The ID of the user to whom the work item is assigned."""

    schedule: ScheduleDefinition | None = None
    """Scheduling properties for the work item."""

    resources: ScheduleResourcesDefinition | None = None
    """Resources reserved for scheduling the work item."""
