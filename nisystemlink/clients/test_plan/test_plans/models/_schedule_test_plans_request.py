from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from ._schedule_test_plans_body_content import ScheduleTestPlanBodyContent


class ScheduleTestPlansRequest(JsonModel):
    """Represents the request body for scheduling multiple test plans."""

    test_plans: Optional[List[ScheduleTestPlanBodyContent]]
    """List of test plan scheduling content objects."""

    replace: Optional[bool] = None
    """(Optional) If true, replaces existing scheduled test plans."""
