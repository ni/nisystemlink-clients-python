from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._create_work_item_template_request import CreateWorkItemTemplateRequest
from ._work_item_template import WorkItemTemplate


class CreateWorkItemTemplatesPartialSuccessResponse(JsonModel):
    """Response for creating work item templates with partial success."""

    created_work_item_templates: List[WorkItemTemplate]
    """List of successfully created work item templates."""

    failed_work_item_templates: List[CreateWorkItemTemplateRequest] | None = None
    """List of work item template requests that failed during creation."""

    error: ApiError | None = None
    """The error that occurred when creating the work item templates."""
