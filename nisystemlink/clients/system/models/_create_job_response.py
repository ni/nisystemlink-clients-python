from typing import Optional

from ._create_job_request import CreateJobRequest
from ._http_error import HttpError


class CreateJobResponse(CreateJobRequest):
    """Model for response of create job request."""

    error: Optional[HttpError] = None
    """Represents the standard error structure."""

    jid: Optional[str] = None
    """The job ID."""
