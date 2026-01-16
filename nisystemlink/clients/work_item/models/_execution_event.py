from datetime import datetime
from typing import Annotated, List, Literal

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._state import State


class ExecutionEventBase(JsonModel):
    """Base class for execution events containing common attributes."""

    action: str | None = None
    """The action the execution was triggered for."""

    triggered_at: datetime | None = None
    """The time the execution was triggered."""

    triggered_by: str | None = None
    """The user who triggered the execution."""

    previous_state: State | None = None
    """The state of the work item at the time of execution."""

    previous_substate: str | None = None
    """The substate of the work item at the time of execution."""

    new_state: State | None = None
    """The state of the work item resulting from execution."""

    new_substate: str | None = None
    """The substate of the work item resulting from execution."""

    error: ApiError | None = None
    """The error from the execution, if any."""


class NotebookExecutionEvent(ExecutionEventBase):
    """An event tracking a notebook execution triggered from a work item."""

    type: Literal["NOTEBOOK"] = Field(default="NOTEBOOK")
    """Type of execution, default is 'NOTEBOOK'."""

    execution_id: str | None = None
    """The ID of the triggered execution."""


class JobExecutionEvent(ExecutionEventBase):
    """An event tracking a job execution triggered from a work item."""

    type: Literal["JOB"] = Field(default="JOB")
    """Type of execution, default is 'JOB'."""

    job_ids: List[str] | None = None
    """The list of job IDs."""


class ManualExecutionEvent(ExecutionEventBase):
    """An event tracking a manual execution triggered from a work item."""

    type: Literal["MANUAL"] = Field(default="MANUAL")
    """Type of execution, default is 'MANUAL'."""


ExecutionEvent = Annotated[
    NotebookExecutionEvent | ManualExecutionEvent | JobExecutionEvent,
    Field(discriminator="type"),
]
