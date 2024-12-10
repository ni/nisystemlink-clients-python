from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._job import Job


class ScheduledJob(Job):
    """Represents a scheduled job."""

    scheduled_timestamp: Optional[datetime] = None
    """The timestamp when the job was scheduled."""

    completed_timestamp: Optional[datetime] = None
    """The timestamp when the job was completed."""


class QueryJobsResponse(JsonModel):
    """Model for response of a query request."""

    error: Optional[ApiError] = None
    """Represents the standard error structure."""

    data: Optional[List[ScheduledJob]] = None
    """The data returned by the query."""

    count: int
    """The total number of resources that matched the query."""
