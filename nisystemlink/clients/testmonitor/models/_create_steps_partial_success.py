from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._step import Step
from nisystemlink.clients.testmonitor.models._create_steps_request import CreateStepRequestObject


class CreateStepsPartialSuccess(JsonModel):
    steps: Optional[List[Step]] = None
    """The list of steps that were successfully created."""

    failed: Optional[List[CreateStepRequestObject]] = None
    """The list of steps that were not created.

    If this is `None`, then all steps were successfully created.
    """

    error: Optional[ApiError] = None
    """Error messages for steps that were not created.

    If this is `None`, then all steps were successfully created.
    """
