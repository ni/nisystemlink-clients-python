from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._schedule_test_plan_request import ScheduleTestPlanRequest
from ._test_plan import TestPlan


class ScheduleTestPlansResponse(JsonModel):
    """Represents the response returned after attempting to schedule one or more test plans."""

    scheduled_test_plans: List[TestPlan] | None = None
    """(Optional) List of successfully scheduled test plans."""

    failed_test_plans: List[ScheduleTestPlanRequest] | None = None
    """(Optional) List of test plan requests that failed to schedule."""

    error: ApiError | None = None
    """The error that occurred when scheduling the test plans."""
