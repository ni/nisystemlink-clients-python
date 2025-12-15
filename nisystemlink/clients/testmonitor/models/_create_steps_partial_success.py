from typing import List

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._create_steps_request import (
    CreateStepRequest,
)
from nisystemlink.clients.testmonitor.models._step import Step


class CreateStepsPartialSuccess(JsonModel):
    steps: List[Step]
    """The list of steps that were successfully created."""

    failed: List[CreateStepRequest] | None = None
    """The list of step requests that failed.

    If this is `None`, then all steps were successfully created.
    """

    error: ApiError | None = None
    """Error messages for steps that were not created.

    If this is `None`, then all steps were successfully created.
    """
