from typing import Dict, Optional, Any

from ._job_config import JobConfig


class CreateJobRequest(JobConfig):
    """An instance of NationalInstruments.SystemsManagementService.Model.API.CreateJobRequest."""

    metadata: Optional[Dict[str, Any]] = None
    """The metadata associated with the job."""
