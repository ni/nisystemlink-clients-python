from datetime import datetime
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ScheduleTestPlanRequest(JsonModel):
    """Represents the request body content for scheduling a test plan."""

    id: str
    """Unique identifier for the test plan to be scheduled."""

    assigned_to: str | None = None
    """(Optional) User or entity to whom the test plan is assigned."""

    dut_id: str | None = None
    """(Optional) Identifier for the Device Under Test (DUT)."""

    system_id: str | None = None
    """(Optional) Identifier for the system where the test plan will run."""

    planned_start_date_time: datetime | None = None
    """(Optional) Planned start date and time for the test plan execution (ISO 8601 format)."""

    estimated_end_date_time: datetime | None = None
    """(Optional) Estimated end date and time for the test plan execution (ISO 8601 format)."""

    estimated_duration_in_seconds: int | None = None
    """(Optional) Estimated duration of the test plan execution in seconds."""

    fixture_ids: List[str] | None = None
    """(Optional) List of fixture identifiers associated with the test plan."""
