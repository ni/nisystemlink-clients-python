from datetime import datetime

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ScheduleDefinition(JsonModel):
    """Scheduling properties for the work item."""

    planned_start_date_time: datetime | None = None
    """The planned start date and time for the work item."""

    planned_end_date_time: datetime | None = None
    """The planned end date and time for the work item."""

    planned_duration_in_seconds: int | None = None
    """The planned duration of the work item in seconds."""
