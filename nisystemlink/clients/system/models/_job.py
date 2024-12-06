from pydantic import Field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


from nisystemlink.clients.core._uplink._json_model import JsonModel


class JobState(Enum):
    """The state of the job."""

    SUCCEEDED = "SUCCEEDED"
    OUTOFQUEUE = "OUTOFQUEUE"
    INQUEUE = "INQUEUE"
    INPROGRESS = "INPROGRESS"
    CANCELED = "CANCELED"
    FAILED = "FAILED"


class JobConfig(JsonModel):
    """The configuration of the job."""

    user: Optional[str] = None
    """The user who created the job."""

    target_systems: Optional[List[str]] = Field(None, alias="tgt")
    """The target systems for the job."""

    functions: Optional[List[str]] = Field(None, alias="fun")
    """Salt functions related to the job."""

    arguments: Optional[List[List[Any]]] = Field(None, alias="args")
    """Arguments of the salt functions."""


class JobResult(JsonModel):
    id: Optional[str] = Field(None, alias="jid")
    """The job ID."""

    system_id: Optional[str] = Field(None, alias="id")
    """The ID of the system that the job targets."""

    return_code: Optional[List[int]] = None
    """Return code of the job."""

    return_: Optional[List[Any]] = None
    """Return value of the job."""

    success: Optional[bool] = None
    """Whether the job was successful."""


class Job(JsonModel):
    """Job Model."""

    id: Optional[str] = Field(None, alias="jid")
    """The job ID."""

    system_id: Optional[str] = Field(None, alias="id")
    """The ID of the system that the job targets."""

    created_timestamp: Optional[datetime] = None
    """The timestamp representing when the job was created."""

    last_updated_timestamp: Optional[datetime] = None
    """The timestamp representing when the job was last updated."""

    dispatched_timestamp: Optional[datetime] = None
    """The timestamp representing when the job was dispatched."""

    state: Optional[JobState] = None
    """The state of the job."""

    metadata: Optional[Dict[str, Any]] = None
    """The metadata associated with the job."""

    config: Optional[JobConfig] = None
    """The configuration of the job."""

    result: Optional[JobResult] = None
    """The result of the job."""

    class Config:
        orm_mode = True
