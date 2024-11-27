from typing import Optional

from ._create_job_request import CreateJobRequest
from ._http_error import HttpError


class CreateJobResponse(CreateJobRequest):
    """The job that was created."""

    error: Optional[HttpError] = None
    """Represents the standard error structure."""

    jid: Optional[str] = None
    """The job ID."""
