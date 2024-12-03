from typing import Optional

from nisystemlink.clients.core import ApiError
from ._create_job_request import CreateJobRequest


class CreateJobResponse(CreateJobRequest):
    """Model for response of create job request."""

    error: Optional[ApiError] = None
    """Represents the standard error structure."""

    jid: Optional[str] = None
    """The job ID."""
