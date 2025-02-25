from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.step.models._create_steps_request import StepRequestObjectBase


class UpdateStepRequestObject(StepRequestObjectBase):
    stepId: Optional[str] = None
    """Step id."""

    resultId: Optional[str] = None
    """Result id."""

    name: Optional[str] = None
    """Step name."""

    children: Optional[List["UpdateStepRequestObject"]] = None
    """Nested child steps."""


class UpdateStepsRequest(JsonModel):
    steps: List[UpdateStepRequestObject]
    """Array of test steps to update."""

    updateResultTotalTime: Optional[bool] = None
    """Determine test result total time from the test step total times."""

    replaceKeywords: Optional[bool] = None
    """Replace with existing keywords instead of merging them."""

    replaceProperties: Optional[bool] = None
    """Replace with existing properties instead of merging them."""
