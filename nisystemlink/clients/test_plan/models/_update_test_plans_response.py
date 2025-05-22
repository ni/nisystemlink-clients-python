from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._test_plan import TestPlan
from ._update_test_plan_request import UpdateTestPlanRequest


class UpdateTestPlansResponse(JsonModel):
    """Represents the response after attempting to update test plans."""

    updated_test_plans: Optional[List[TestPlan]] = None
    """List of successfully updated test plans."""

    failed_test_plans: Optional[List[UpdateTestPlanRequest]] = None
    """List of test plans that failed to update."""

    error: Optional[ApiError] = None
    """The error that occurred when updating the test plans."""
