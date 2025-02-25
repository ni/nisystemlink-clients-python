from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.step.models import StepIdResultIdPair


class DeleteStepsRequest(JsonModel):
    steps: List[StepIdResultIdPair]
    """Array of test step id and result id pairs to delete."""
