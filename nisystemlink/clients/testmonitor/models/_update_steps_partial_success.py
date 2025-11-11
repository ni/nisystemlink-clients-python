from typing import List

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._step import Step
from nisystemlink.clients.testmonitor.models._update_steps_request import (
    UpdateStepRequest,
)


class UpdateStepsPartialSuccess(JsonModel):
    steps: List[Step]
    """The list of steps that were successfully updated."""

    failed: List[UpdateStepRequest] | None = None
    """The list of steps that were not updated.

    If this is `None`, then all steps were successfully updated.
    """

    error: ApiError | None = None
    """Error messages for steps that were not updated.

    If this is `None`, then all steps were successfully updated.
    """
