from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._work_item_template import WorkItemTemplate


class UpdateWorkItemTemplatesResponse(JsonModel):
    """Response information for the update work item templates API."""

    updated_work_item_templates: List[WorkItemTemplate]
    """List of updated work item templates."""
