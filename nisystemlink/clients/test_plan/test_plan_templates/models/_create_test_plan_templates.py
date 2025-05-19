

from typing import List, Optional
from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from ._test_plan_templates import TestPlanTemplateBase, TestPlanTemplateResponse


class CreateTestPlanTemplate(JsonModel):
    """Creates one or more test plan templates with the provided data."""

    testPlanTemplates: List[TestPlanTemplateBase]
    """List of test plan templates to create."""

class CreateTestPlanTemplateResponse(JsonModel):

    createdTestPlanTemplates: Optional[List[TestPlanTemplateResponse]] = None
    """The list of test plan templates that were successfully created."""

    failedTestPlanTemplates: Optional[List[TestPlanTemplateResponse]] = None
    """The list of test plan templates that were not created.

    If this is `None`, then all test plan templates were successfully created.
    """

    error: Optional[ApiError] = None
    """Error messages for test plan templates that were not created.

    If this is `None`, then all test plan templates were successfully created.
    """