from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._create_test_plan_template_request import CreateTestPlanTemplateRequest
from ._test_plan_templates import TestPlanTemplate


class CreateTestPlanTemplatePartialSuccessResponse(JsonModel):

    created_test_plan_templates: List[TestPlanTemplate] | None = None
    """The list of test plan templates that were successfully created."""

    failed_test_plan_templates: List[CreateTestPlanTemplateRequest] | None = None
    """The list of test plan templates that were not created.

    If this is `None`, then all test plan templates were successfully created.
    """

    error: ApiError | None = None
    """Error messages for test plan templates that were not created.

    If this is `None`, then all test plan templates were successfully created.
    """
