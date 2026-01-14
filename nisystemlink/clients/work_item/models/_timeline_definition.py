from datetime import datetime

from nisystemlink.clients.core._uplink._json_model import JsonModel


class TimelineDefinition(JsonModel):
    """Timeline properties for the work item."""

    earliest_start_date_time: datetime | None = None
    """The earliest start date and time for the work item."""

    due_date_time: datetime | None = None
    """The due date and time for the work item."""

    estimated_duration_in_seconds: int | None = None
    """The estimated duration of the work item in seconds."""


class TemplateTimelineDefinition(JsonModel):
    """Timeline properties for the work item created from a template."""

    estimated_duration_in_seconds: int | None = None
    """The estimated duration of the work item in seconds."""
