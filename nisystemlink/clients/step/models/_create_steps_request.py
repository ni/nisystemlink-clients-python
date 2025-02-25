from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.step.models import (
    NamedValueObject,
    StatusObject,
    StepDataObject,
)


class StepRequestObjectBase(JsonModel):
    parentId: Optional[str] = None
    """Parent step id."""

    children: Optional[List["CreateStepRequestObject"]] = None
    """Nested child steps."""

    data: Optional[StepDataObject] = None
    """Data returned by the test step."""

    dataModel: Optional[str] = None
    """Data model for the step."""

    startedAt: Optional[datetime] = None
    """ISO-8601 formatted timestamp indicating when the test result began."""

    status: Optional[StatusObject] = None
    """The status of the step."""

    stepType: Optional[str] = None
    """Step type."""

    totalTimeInSeconds: Optional[float] = None
    """Total number of seconds the step took to execute."""

    inputs: Optional[List[NamedValueObject]] = None
    """Inputs and their values passed to the test."""

    outputs: Optional[List[NamedValueObject]] = None
    """Outputs and their values logged by the test."""

    keywords: Optional[List[str]] = None
    """Words or phrases associated with the step."""

    properties: Optional[dict] = None
    """Test step properties."""


class CreateStepRequestObject(StepRequestObjectBase):
    stepId: str
    """Step id."""

    resultId: str
    """Result id."""

    name: str
    """Step name."""


class CreateStepsRequest(JsonModel):
    steps: List[CreateStepRequestObject]
    """Array of test steps to create."""

    updateResultTotalTime: Optional[bool] = None
    """Determine test result total time from the test step total times."""
