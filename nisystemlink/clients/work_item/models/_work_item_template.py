from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import Dashboard
from ._execution_definition import ExecutionDefinition
from ._resources_definition import TemplateResourcesDefinition
from ._timeline_definition import TemplateTimelineDefinition


class WorkItemTemplateBase(JsonModel):
    """Contains information about a work item template."""

    name: str | None = None
    """The name of the work item template."""

    template_group: str | None = None
    """The template group defined by the user."""

    type: str | None = None
    """The type of work item created from this template."""

    product_families: List[str] | None = None
    """The array of product families to which the work item template belongs."""

    part_numbers: List[str] | None = None
    """The array of part numbers of the products linked to the work item template."""

    summary: str | None = None
    """The summary of the work item template."""

    description: str | None = None
    """The description of the work item created from this template."""

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

    dashboard: Dashboard | None = None
    """The dashboard data related to the work item created from this template."""

    workflow_id: str | None = None
    """The ID of the workflow associated with the work item created from this template."""


class WorkItemTemplate(WorkItemTemplateBase):
    """Contains response information for work item template."""

    id: str | None = None
    """The ID of the work item template."""

    name: str | None = None
    """The name of the work item template."""

    created_by: str | None = None
    """The user who created the work item template."""

    updated_by: str | None = None
    """The user who last updated the work item template."""

    created_at: datetime | None = None
    """The date and time when the work item template was created."""

    updated_at: datetime | None = None
    """The date and time when the work item template was last updated."""
