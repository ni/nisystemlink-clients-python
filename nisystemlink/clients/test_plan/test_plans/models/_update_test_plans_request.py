from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from . import UpdateTestPlanBodyContent


class UpdateTestPlansRequest(JsonModel):
    """Represents the request body for updating multiple test plans."""

    test_plans: List[UpdateTestPlanBodyContent]
    """A list of test plans to update."""

    replace: Optional[bool] = None
    """Whether to replace the existing test plans or update them."""
