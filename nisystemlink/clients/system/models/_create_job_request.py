from typing import Dict, Optional, Any

from ._job_config import JobConfig


class CreateJobRequest(JobConfig):
    """Model for create job request."""

    metadata: Optional[Dict[str, Any]] = None
    """The metadata associated with the job."""
