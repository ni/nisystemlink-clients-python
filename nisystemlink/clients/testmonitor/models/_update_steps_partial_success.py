from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._step import Step
from nisystemlink.clients.testmonitor.models._update_steps_request import (
    UpdateStepRequestObject,
)


class UpdateStepsPartialSuccess(JsonModel):
    steps: Optional[List[Step]] = None
    """The list of steps that were successfully updated."""

    failed: Optional[List[UpdateStepRequestObject]] = None
    """The list of steps that were not updated.

    If this is `None`, then all steps were successfully updated.
    """

    error: Optional[ApiError] = None
    """Error messages for steps that were not updated.

    If this is `None`, then all steps were successfully updated.
    """
