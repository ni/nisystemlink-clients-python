from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import Dashboard
from ._execution_definition import ExecutionDefinition
from ._resources_definition import ResourcesDefinition
from ._timeline_definition import TimelineDefinition


class CreateWorkItemRequest(JsonModel):
    """Represents the request body content for creating a work item."""

    name: str | None = None
    """The name of the work item."""

    type: str | None = None
    """The type of the work item."""

    state: str | None = None
    """The state of the work item."""

    description: str | None = None
    """A description of the work item."""

    parent_id: str | None = None
    """The ID of the parent work item."""

    template_id: str | None = None
    """The ID of the template used to create the work item."""

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

    resources: ResourcesDefinition | None = None
    """Resources reserved for the work item."""

    execution_actions: List[ExecutionDefinition] | None = None
    """The execution actions defined for the work item."""

    file_ids_from_template: List[str] | None = None
    """The list of file IDs inherited from the template."""

    properties: Dict[str, str] | None = None
    """Additional properties for the work item."""

    dashboard: Dashboard | None = None
    """The dashboard associated with the work item."""

    workflow_id: str | None = None
    """The ID of the workflow associated with the work item."""
