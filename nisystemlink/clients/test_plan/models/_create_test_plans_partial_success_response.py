from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._create_test_plan_request import CreateTestPlanRequest
from ._test_plan import TestPlan


class CreateTestPlansPartialSuccessResponse(JsonModel):
    """Represents the response from creating test plans, including successfully created,
    failed test plans, and any associated errors.
    """

    created_test_plans: Optional[List[TestPlan]] = None
    """List of test plans that were successfully created."""

    failed_test_plans: Optional[List[CreateTestPlanRequest]] = None
    """List of test plans that failed to be created, with their request body content."""

    error: Optional[ApiError] = None
    """The error that occurred when creating the test plans."""
