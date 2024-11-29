from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._http_error import HttpError


class JobSummaryResponse(JsonModel):
    """Model for request of jobs summary response."""

    error: Optional[HttpError] = None
    """Represents the standard error structure."""

    active_count: Optional[int] = None
    """The number of active jobs."""

    failed_count: Optional[int] = None
    """The number of failed jobs."""

    succeeded_count: Optional[int] = None
    """The number of succeeded jobs."""
