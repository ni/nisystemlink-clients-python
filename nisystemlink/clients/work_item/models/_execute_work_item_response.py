from typing import Literal

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class ExecuteWorkItemResult(JsonModel):
    """Represents the result of a work item execution action."""

    type: Literal["MANUAL", "JOB", "NOTEBOOK", "NONE"]
    """Type of execution that was triggered (MANUAL, JOB, NOTEBOOK, or NONE)."""

    execution_id: str | None = None
    """The execution ID if applicable."""

    error: ApiError | None = None
    """Error information if the execution encountered an error."""


class ExecuteWorkItemResponse(JsonModel):
    """Response for executing a work item action."""

    error: ApiError | None = None
    """Error information if the action failed."""

    result: ExecuteWorkItemResult | None = None
    """Result of the action execution."""
