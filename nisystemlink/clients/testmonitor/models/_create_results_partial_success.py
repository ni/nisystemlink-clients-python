from typing import List

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._create_result_request import (
    CreateResultRequest,
)
from nisystemlink.clients.testmonitor.models._result import Result


class CreateResultsPartialSuccess(JsonModel):
    results: List[Result]
    """The list of results that were successfully created."""

    failed: List[CreateResultRequest] | None = None
    """The list of results that were not created.
    If this is `None`, then all results were successfully created.
    """

    error: ApiError | None = None
    """Error messages for results that were not created.
    If this is `None`, then all results were successfully created.
    """
