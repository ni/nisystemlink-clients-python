from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import DashboardUrl
from ._execution_definition import ExecutionDefinition
from ._resources_definition import TemplateResourcesDefinition
from ._timeline_definition import TemplateTimelineDefinition


class UpdateWorkItemTemplateRequest(JsonModel):
    """Represents the request body content for updating a single work item template."""

    id: str
    """The ID of the work item template."""

    product_families: List[str] | None = None
    """The array of product families to which the work item template belongs."""

    part_numbers: List[str] | None = None
    """The array of part numbers of the products linked to the work item template."""

    name: str | None = None
    """The name of the work item template."""

    summary: str | None = None
    """The summary of the work item template."""

    description: str | None = None
    """The description of the work item created from this template."""

    template_group: str | None = None
    """The template group defined by the user."""

    test_program: str | None = None
    """The test program associated with the work item created from this template."""

    timeline: TemplateTimelineDefinition | None = None
    """Timeline properties for the work item created from this template."""

    resources: TemplateResourcesDefinition | None = None
    """Resources selection criteria for the work item created from this template."""

    execution_actions: List[ExecutionDefinition] | None = None
    """The execution actions defined for the work item."""

    file_ids: List[str] | None = None
    """The array of file IDs associated with the work item template."""

    workspace: str | None = None
    """The workspace to which the work item template belongs."""

    properties: Dict[str, str] | None = None
    """Additional properties associated with the work item created from this template."""

    dashboard: DashboardUrl | None = None
    """The dashboard data related to the work item created from this template."""

    workflow_id: str | None = None
    """The ID of the workflow associated with the work item created from this template."""
