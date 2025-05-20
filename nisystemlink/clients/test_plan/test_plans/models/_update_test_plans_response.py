from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from . import TestPlan, UpdateTestPlanBodyContent


class UpdateTestPlansResponse(JsonModel):
    """Represents the response after attempting to update test plans."""

    updated_test_plans: Optional[List[TestPlan]] = None
    """List of successfully updated test plans."""

    failed_test_plans: Optional[List[UpdateTestPlanBodyContent]] = None
    """List of test plans that failed to update."""

    error: Optional[ApiError] = None
    """Error information if the update operation failed."""
