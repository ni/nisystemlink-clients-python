from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._resources_definition import ResourcesDefinition
from ._timeline_definition import TimelineDefinition


class UpdateWorkItemRequest(JsonModel):
    """Represents the request body content for updating a single work item."""

    id: str
    """The ID of the work item to update."""

    name: str | None = None
    """The new name for the work item."""

    state: str | None = None
    """The new state of the work item."""

    description: str | None = None
    """The new description for the work item."""

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

    resources: ResourcesDefinition | None = None
    """Resources reserved for the work item."""

    properties: Dict[str, str] | None = None
    """Additional properties for the work item as key-value pairs."""

    file_ids_from_template: List[str] | None = None
    """List of file IDs from the template to associate with the work item."""
