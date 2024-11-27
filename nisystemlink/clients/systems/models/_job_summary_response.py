from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._http_error import HttpError


class JobSummaryResponse(JsonModel):
    """Model for request of jobs summary response."""

    error: Optional[HttpError] = None
    """Represents the standard error structure."""

    activeCount: Optional[int] = None
    """The number of active jobs."""

    failedCount: Optional[int] = None
    """The number of failed jobs."""

    succeededCount: Optional[int] = None
    """The number of succeeded jobs."""
