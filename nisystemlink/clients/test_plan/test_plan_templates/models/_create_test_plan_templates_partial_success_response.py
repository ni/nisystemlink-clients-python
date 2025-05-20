from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._test_plan_templates import TestPlanTemplateBase, TestPlanTemplateResponse


class CreateTestPlanTemplatePartialSuccessResponse(JsonModel):

    created_test_plan_templates: Optional[List[TestPlanTemplateResponse]] = None
    """The list of test plan templates that were successfully created."""

    failed_test_plan_templates: Optional[List[TestPlanTemplateBase]] = None
    """The list of test plan templates that were not created.

    If this is `None`, then all test plan templates were successfully created.
    """

    error: Optional[ApiError] = None
    """Error messages for test plan templates that were not created.

    If this is `None`, then all test plan templates were successfully created.
    """
