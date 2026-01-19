from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import DashboardUrl
from ._execution_definition import ExecutionDefinition
from ._execution_event import ExecutionEvent
from ._resources_definition import ResourcesDefinition
from ._schedule_definition import ScheduleDefinition
from ._state import State
from ._timeline_definition import TimelineDefinition


class WorkItem(JsonModel):
    """Contains information about a work item."""

    id: str | None = None
    """The ID of the work item."""

    template_id: str | None = None
    """The ID of the template used to create the work item."""

    name: str | None = None
    """The name of the work item."""

    type: str | None = None
    """The type of the work item."""

    state: State | None = None
    """The state of the work item."""

    substate: str | None = None
    """The substate of the work item, if any."""

    description: str | None = None
    """The description of the work item."""

    parent_id: str | None = None
    """The ID of the parent work item."""

    assigned_to: str | None = None
    """The user or group assigned to the work item."""

    requested_by: str | None = None
    """The user or group who requested the work item."""

    test_program: str | None = None
    """The test program associated with the work item."""

    part_number: str | None = None
    """The part number associated with the work item."""

    workspace: str | None = None
    """The workspace to which the work item belongs."""

    timeline: TimelineDefinition | None = None
    """Timeline properties for the work item."""

    schedule: ScheduleDefinition | None = None
    """Scheduling properties for the work item."""

    resources: ResourcesDefinition | None = None
    """Resources reserved for the work item."""

    created_by: str | None = None
    """The user who created the work item."""

    updated_by: str | None = None
    """The user who last updated the work item."""

    created_at: datetime | None = None
    """The date and time when the work item was created."""

    updated_at: datetime | None = None
    """The date and time when the work item was last updated."""

    properties: Dict[str, str] | None = None
    """Additional properties associated with the work item."""

    file_ids_from_template: List[str] | None = None
    """The list of file IDs inherited from the template."""

    dashboard: DashboardUrl | None = None
    """The dashboard data related to the work item."""

    execution_actions: List[ExecutionDefinition] | None = None
    """The execution actions defined for the work item."""

    execution_history: List[ExecutionEvent] | None = None
    """The execution history of the work item."""

    workflow_id: str | None = None
    """The ID of the workflow associated with the work item."""
