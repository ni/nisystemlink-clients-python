from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._create_steps_request import (
    BaseStepRequest,
)


class UpdateStepRequest(BaseStepRequest):
    name: Optional[str] = None
    """Step name."""

    children: Optional[List["UpdateStepRequest"]] = None
    """Nested child steps."""


class UpdateMultipleStepsRequest(JsonModel):
    steps: List[UpdateStepRequest]
    """List of test steps to update."""

    update_result_total_time: Optional[bool] = None
    """Determine test result total time from the test step total times."""

    replace_keywords: Optional[bool] = None
    """Replace with existing keywords instead of merging them."""

    replace_properties: Optional[bool] = None
    """Replace with existing properties instead of merging them."""
