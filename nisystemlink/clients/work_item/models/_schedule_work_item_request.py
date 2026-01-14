from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._schedule_definition import ScheduleDefinition
from ._resources_definition import ScheduleResourcesDefinition


class ScheduleWorkItemRequest(JsonModel):
    """Represents the request body content for scheduling a single work item."""

    id: str
    """The ID of the work item to be scheduled."""

    assigned_to: str | None = None
    """The ID of the user to whom the work item is assigned."""

    schedule: ScheduleDefinition | None = None
    """The scheduling properties for the work item."""

    resources: ScheduleResourcesDefinition | None = None
    """The resources reserved for the work item."""