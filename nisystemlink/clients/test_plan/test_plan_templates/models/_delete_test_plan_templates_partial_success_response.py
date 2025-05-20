from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteTestPlanTemplatesPartialSuccessResponse(JsonModel):
    """The result of deleting multiple test plan templates
    when one or more test plan templates could not be deleted.
    """

    deleted_test_plan_template_ids: List[str]
    """The IDs of the test plan template that could not be deleted."""

    failed_test_plan_template_ids: Optional[List[str]] = None
    """The IDs of the test plan template that could not be deleted."""

    error: Optional[ApiError] = None
    """The error that occurred when deleting the test plan template."""
