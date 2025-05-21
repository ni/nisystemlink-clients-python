from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._create_test_plan_body_content import CreateTestPlanBodyContent
from ._test_plan import TestPlan


class CreateTestPlansResponse(JsonModel):
    """Represents the response from creating test plans, including successfully created,
    failed test plans, and any associated errors.
    """

    test_plans: Optional[List[TestPlan]] = None
    """List of all test plans involved in the operation."""

    created_test_plans: Optional[List[TestPlan]] = None
    """List of test plans that were successfully created."""

    failed_test_plans: Optional[List[CreateTestPlanBodyContent]] = None
    """List of test plans that failed to be created, with their request body content."""
