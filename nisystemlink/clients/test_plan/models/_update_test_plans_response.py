from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._test_plan import TestPlan
from ._update_test_plan_request import UpdateTestPlanRequest


class UpdateTestPlansResponse(JsonModel):
    """Represents the response after attempting to update test plans."""

    updated_test_plans: List[TestPlan] | None = None
    """List of successfully updated test plans."""

    failed_test_plans: List[UpdateTestPlanRequest] | None = None
    """List of test plans that failed to update."""

    error: ApiError | None = None
    """The error that occurred when updating the test plans."""
