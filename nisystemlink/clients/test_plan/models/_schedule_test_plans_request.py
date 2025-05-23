from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._schedule_test_plan_request import ScheduleTestPlanRequest


class ScheduleTestPlansRequest(JsonModel):
    """Represents the request body for scheduling multiple test plans."""

    test_plans: List[ScheduleTestPlanRequest]
    """List of test plan scheduling content objects."""

    replace: Optional[bool] = None
    """(Optional) If true, replaces existing scheduled test plans."""
