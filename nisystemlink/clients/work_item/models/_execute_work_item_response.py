from typing import List, Literal

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class ExecutionResult(JsonModel):
    """Result of executing a work item action."""

    type: Literal["NONE", "MANUAL", "NOTEBOOK", "JOB", "SCHEDULE", "UNSCHEDULE"]
    """Type of execution."""

    error: ApiError | None = None
    """Error information if the execution encountered an error."""

    execution_id: str | None = None
    """The notebook execution ID. Only populated when type is NOTEBOOK."""

    job_ids: List[str] | None = None
    """The list of job IDs. Only populated when type is JOB."""


class ExecuteWorkItemResponse(JsonModel):
    """Response for executing a work item action."""

    error: ApiError | None = None
    """Error information if the action failed."""

    result: ExecutionResult | None = None
    """Result of the action execution."""
