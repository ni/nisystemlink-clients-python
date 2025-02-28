from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Extra


class StatusType(str, Enum):
    """The types of statuses that a result can have."""

    LOOPING = "LOOPING"
    SKIPPED = "SKIPPED"
    CUSTOM = "CUSTOM"
    DONE = "DONE"
    PASSED = "PASSED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"
    ERRORED = "ERRORED"
    TIMED_OUT = "TIMED_OUT"


class ResultStatus(JsonModel):
    """Contains information about a status object."""

    status_type: StatusType
    """The type of status."""

    status_name: Optional[str]
    """The name of the status."""


class StandardResultStatus:
    LOOPING = ResultStatus(status_type=StatusType.LOOPING)
    SKIPPED = ResultStatus(status_type=StatusType.SKIPPED)
    DONE = ResultStatus(status_type=StatusType.DONE)
    PASSED = ResultStatus(status_type=StatusType.PASSED)
    FAILED = ResultStatus(status_type=StatusType.FAILED)
    RUNNING = ResultStatus(status_type=StatusType.RUNNING)
    WAITING = ResultStatus(status_type=StatusType.WAITING)
    TERMINATED = ResultStatus(status_type=StatusType.TERMINATED)
    ERRORED = ResultStatus(status_type=StatusType.ERRORED)
    TIMED_OUT = ResultStatus(status_type=StatusType.TIMED_OUT)


class Result(JsonModel):
    """Contains information about a result."""

    status: Optional[ResultStatus]
    """The status of the result."""

    started_at: Optional[datetime]
    """The time that the result started."""

    updated_at: Optional[datetime]
    """The last time that this result was updated."""

    program_name: Optional[str]
    """The name of the program that generated this result."""

    id: Optional[str]
    """The globally unique id of the result."""

    system_id: Optional[str]
    """The id of the system that generated this result."""

    host_name: Optional[str]
    """The name of the host that generated this result."""

    part_number: Optional[str]
    """The part number is the unique identifier of a product within a single org."""

    serial_number: Optional[str]
    """The serial number of the system that generated this result."""

    total_time_in_seconds: Optional[float]
    """The total time that the result took to run in seconds."""

    keywords: Optional[List[str]]
    """A list of keywords that categorize this result."""

    properties: Optional[Dict[str, str]]
    """A list of custom properties for this result."""

    operator: Optional[str]
    """The operator that ran the result."""

    file_ids: Optional[List[str]]
    """A list of file ids that are attached to this result."""

    data_table_ids: Optional[List[str]]
    """A list of data table ids that are attached to this result."""

    status_type_summary: Optional[Dict[StatusType, int]]
    """A summary of the status types in the result."""

    workspace: Optional[str]
    """The id of the workspace that this product belongs to."""

    class Config:
        extra = Extra.ignore
