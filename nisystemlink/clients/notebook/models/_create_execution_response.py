from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._execution import Execution


class CreatedExecution(Execution):
    cached_result: bool
    """Returns true if the execution is returned from cache"""


class CreateExecutionsResponse(JsonModel):
    """Model for response to a request to create an execution."""

    error: Optional[ApiError] = None
    """The error that occurred during the request, if any."""

    executions: Optional[List[CreatedExecution]] = None
    """Gets or sets the collection of authorized executions."""
