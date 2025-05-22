from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._create_test_plan_request import CreateTestPlanRequest


class CreateTestPlansRequest(JsonModel):
    """Represents the request body for creating multiple test plans."""

    test_plans: Optional[List[CreateTestPlanRequest]] = None
    """
    A list of test plan creation request bodies. Each item in the list contains
    the content required to create an individual test plan.
    """
