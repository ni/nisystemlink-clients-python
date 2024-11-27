from typing import Dict, List, Optional
from datetime import datetime

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._job_state import JobState
from ._job_config import JobConfig


class JobResult(JsonModel):
    jid: Optional[str] = None
    """The job ID."""

    id: Optional[str] = None
    """The ID of the system that the job targets."""

    retcode: Optional[List[int]] = None
    """Return code of the job."""

    return_: Optional[List[str]] = None
    """Return value of the job."""

    success: Optional[bool] = None
    """Whether the job was successful."""


class Job(JsonModel):
    """Job Model."""

    jid: Optional[str] = None
    """The job ID."""

    id: Optional[str] = None
    """The ID of the system that the job targets."""

    created_timestamp: Optional[datetime] = None
    """The timestamp representing when the job was created."""

    last_updated_timestamp: Optional[datetime] = None
    """The timestamp representing when the job was last updated."""

    dispatched_timestamp: Optional[datetime] = None
    """The timestamp representing when the job was dispatched."""

    state: Optional[JobState] = None
    """The state of the job."""

    metadata: Optional[Dict[str, str]] = None
    """The metadata associated with the job."""

    config: Optional[JobConfig] = None
    """The configuration of the job."""

    result: Optional[JobResult] = None
    """The result of the job."""