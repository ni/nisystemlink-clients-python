from datetime import datetime
from pydantic import Field
from typing import List, Optional, Dict, Any

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._job import JobState, JobResult


class QueryJobConfig(JsonModel):
    """The configuration of the job."""

    user: Optional[str] = None
    """The user who created the job."""

    target_systems: Optional[List[str]] = Field(None, alias="tgt")
    """The target systems for the job."""

    functions: Optional[List[str]] = Field(None, alias="fun")
    """Salt functions related to the job."""

    arguments: Optional[List[List[Any]]] = Field(None, alias="arg")
    """Arguments of the salt functions."""


class QueryJob(JsonModel):
    """Job Modal for query response."""

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

    scheduled_timestamp: Optional[datetime] = None
    """The timestamp when the job was scheduled."""

    completing_timestamp: Optional[datetime] = None
    """The timestamp when the job was completed."""

    state: Optional[JobState] = None
    """The state of the job."""

    metadata: Optional[Dict[str, Any]] = None
    """The metadata associated with the job."""

    config: Optional[QueryJobConfig] = None
    """The configuration of the job."""

    result: Optional[JobResult] = None
    """The result of the job."""


class QueryJobsResponse(JsonModel):
    """Model for response of a query request."""

    error: Optional[ApiError] = None
    """Represents the standard error structure."""

    data: Optional[List[QueryJob]] = None
    """The data returned by the query."""

    count: Optional[int] = None
    """The total number of resources that matched the query."""
