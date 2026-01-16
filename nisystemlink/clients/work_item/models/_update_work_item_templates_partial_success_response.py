from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._update_work_item_template_request import UpdateWorkItemTemplateRequest
from ._work_item_template import WorkItemTemplate


class UpdateWorkItemTemplatesPartialSuccessResponse(JsonModel):
    """Response for updating work item templates with partial success."""

    updated_work_item_templates: List[WorkItemTemplate]
    """List of successfully updated work item templates."""

    failed_work_item_templates: List[UpdateWorkItemTemplateRequest] | None = None
    """List of work item template requests that failed to update."""

    error: ApiError | None = None
    """The error that occurred when updating the work item templates."""
