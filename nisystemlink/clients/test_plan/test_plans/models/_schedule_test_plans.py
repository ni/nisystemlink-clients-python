from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from ._test_plan import TestPlan


class ScheduleTestPlanRequestBodyContent(JsonModel):
    """Represents the request body content for scheduling a test plan."""

    id: str
    """Unique identifier for the test plan to be scheduled."""

    assigned_to: Optional[str] = None
    """(Optional) User or entity to whom the test plan is assigned."""

    dut_id: Optional[str] = None
    """(Optional) Identifier for the Device Under Test (DUT)."""

    system_id: Optional[str] = None
    """(Optional) Identifier for the system where the test plan will run."""

    planned_start_date_time: Optional[str] = None
    """(Optional) Planned start date and time for the test plan execution (ISO 8601 format)."""

    estimated_end_date_time: Optional[str] = None
    """(Optional) Estimated end date and time for the test plan execution (ISO 8601 format)."""

    estimated_duration_in_seconds: Optional[int] = None
    """(Optional) Estimated duration of the test plan execution in seconds."""

    fixture_ids: Optional[List[str]] = None
    """(Optional) List of fixture identifiers associated with the test plan."""


class ScheduleTestPlansRequest(JsonModel):
    """Represents the request body for scheduling multiple test plans."""

    test_plans: List[ScheduleTestPlanRequestBodyContent]
    """List of test plan scheduling content objects."""

    replace: Optional[bool] = None
    """(Optional) If true, replaces existing scheduled test plans."""


class ScheduleTestPlansResponse(JsonModel):
    """Represents the response returned after attempting to schedule one or more test plans."""

    scheduled_test_plans: Optional[List[TestPlan]] = None
    """(Optional) List of successfully scheduled test plans."""

    failed_test_plans: Optional[List[ScheduleTestPlanRequestBodyContent]] = None
    """(Optional) List of test plan requests that failed to schedule."""

    error: Optional[ApiError] = None
    """(Optional) API error information if scheduling failed."""
