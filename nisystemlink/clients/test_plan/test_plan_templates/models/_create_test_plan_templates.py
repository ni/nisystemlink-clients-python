

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

    failedTestPlanTemplates: Optional[List[TestPlanTemplateResponse]] = None

    error: Optional[ApiError] = None