from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class StepIdResultIdPair(JsonModel):
    step_id: str
    """The ID of the step."""

    result_id: str
    """The ID of the result associated with the step."""


class DeleteStepsPartialSuccess(JsonModel):
    """The result of deleting multiple steps when one or more steps could not be deleted."""

    steps: List[StepIdResultIdPair]
    """The step_id and result_id pairs of the steps that were successfully deleted."""

    failed: Optional[List[StepIdResultIdPair]] = None
    """The step_id and result_id pairs of the steps that could not be deleted."""

    error: Optional[ApiError] = None
    """The error that occurred when deleting the steps."""
