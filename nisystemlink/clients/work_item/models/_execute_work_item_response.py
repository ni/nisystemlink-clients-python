from typing import Annotated, List, Literal

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class ExecutionResultBase(JsonModel):
    """Base class for execution results containing common attributes."""

    error: ApiError | None = None
    """Error information if the execution encountered an error."""


class NoneExecutionResult(ExecutionResultBase):
    """Result of executing a work item action with no execution implementation."""

    type: Literal["NONE"] = Field(default="NONE")
    """Type of execution."""


class ManualExecutionResult(ExecutionResultBase):
    """Result of executing a manual work item action."""

    type: Literal["MANUAL"] = Field(default="MANUAL")
    """Type of execution."""


class NotebookExecutionResult(ExecutionResultBase):
    """Result of executing a notebook work item action."""

    type: Literal["NOTEBOOK"] = Field(default="NOTEBOOK")
    """Type of execution."""

    execution_id: str | None = None
    """The notebook execution ID."""


class JobExecutionResult(ExecutionResultBase):
    """Result of executing a job work item action."""

    type: Literal["JOB"] = Field(default="JOB")
    """Type of execution."""

    job_ids: List[str] | None = None
    """The list of job IDs."""


class ScheduleExecutionResult(ExecutionResultBase):
    """Result of executing a schedule work item action."""

    type: Literal["SCHEDULE"] = Field(default="SCHEDULE")
    """Type of execution."""


class UnscheduleExecutionResult(ExecutionResultBase):
    """Result of executing an unschedule work item action."""

    type: Literal["UNSCHEDULE"] = Field(default="UNSCHEDULE")
    """Type of execution."""


ExecutionResult = Annotated[
    NoneExecutionResult
    | ManualExecutionResult
    | NotebookExecutionResult
    | JobExecutionResult
    | ScheduleExecutionResult
    | UnscheduleExecutionResult,
    Field(discriminator="type"),
]
"""Result of executing a work item action."""


class ExecuteWorkItemResponse(JsonModel):
    """Response for executing a work item action."""

    error: ApiError | None = None
    """Error information if the action failed."""

    result: ExecutionResult | None = None
    """Result of the action execution."""
