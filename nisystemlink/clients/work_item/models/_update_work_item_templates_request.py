from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._update_work_item_template_request import UpdateWorkItemTemplateRequest


class UpdateWorkItemTemplatesRequest(JsonModel):
    """Represents the request body content for updating multiple work item templates."""

    work_item_templates: List[UpdateWorkItemTemplateRequest]
    """List of work item templates to update."""

    replace: bool | None = None
    """When true, existing key-value pair fields are replaced instead of merged."""
