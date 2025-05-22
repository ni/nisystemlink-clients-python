from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ScheduleTestPlanRequest(JsonModel):
    """Represents the request body content for scheduling a test plan."""

    id: str
    """Unique identifier for the test plan to be scheduled."""

    assigned_to: Optional[str] = None
    """(Optional) User or entity to whom the test plan is assigned."""

    dut_id: Optional[str] = None
    """(Optional) Identifier for the Device Under Test (DUT)."""

    system_id: Optional[str] = None
    """(Optional) Identifier for the system where the test plan will run."""

    planned_start_date_time: Optional[datetime] = None
    """(Optional) Planned start date and time for the test plan execution (ISO 8601 format)."""

    estimated_end_date_time: Optional[datetime] = None
    """(Optional) Estimated end date and time for the test plan execution (ISO 8601 format)."""

    estimated_duration_in_seconds: Optional[int] = None
    """(Optional) Estimated duration of the test plan execution in seconds."""

    fixture_ids: Optional[List[str]] = None
    """(Optional) List of fixture identifiers associated with the test plan."""
