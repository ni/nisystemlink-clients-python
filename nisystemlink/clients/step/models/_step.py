from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class StatusType(str, Enum):
    """The types of statuses that a step can have."""

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


class StatusObject(JsonModel):
    statusType: StatusType
    """The type of status."""

    statusName: Optional[str] = None
    """The name of the status."""


class NamedValueObject(JsonModel):
    name: str
    """The name of the value."""

    value: Any
    """The value."""


class StepDataObject(JsonModel):
    text: Optional[str] = None
    """Text string describing the output data."""

    parameters: Optional[List[dict[str, str]]] = None
    """Array of properties objects."""


class Step(JsonModel):
    name: Optional[str] = None
    """The name of the step."""

    stepType: Optional[str] = None
    """The type of the step."""

    stepId: Optional[str] = None
    """The ID of the step."""

    parentId: Optional[str] = None
    """The ID of the parent step."""

    resultId: Optional[str] = None
    """The ID of the result associated with the step."""

    path: Optional[str] = None
    """The path of the step."""

    pathIds: Optional[List[str]] = None
    """The IDs of the steps in the path."""

    status: Optional[StatusObject] = None
    """The status of the step."""

    totalTimeInSeconds: Optional[int] = None
    """The total time in seconds the step took to execute."""

    startedAt: Optional[datetime] = None
    """The ISO-8601 formatted timestamp indicating when the step started."""

    updatedAt: Optional[datetime] = None
    """The ISO-8601 formatted timestamp indicating when the step was last updated."""

    inputs: Optional[List[NamedValueObject]] = None
    """Inputs and their values passed to the test."""

    outputs: Optional[List[NamedValueObject]] = None
    """Outputs and their values logged by the test."""

    dataModel: Optional[str] = None
    """Custom string defining the model of the data object."""

    data: Optional[StepDataObject] = None
    """Data returned by the test step."""

    hasChildren: Optional[bool] = None
    """Indicates if the step has child steps."""

    workspace: Optional[str] = None
    """The workspace the test step belongs to."""

    keywords: Optional[List[str]] = None
    """Words or phrases associated with the test step."""

    properties: Optional[List[NamedValueObject]] = None
    """Test step properties."""
