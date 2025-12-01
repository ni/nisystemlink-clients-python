from datetime import datetime
from typing import Annotated, List, Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class ExecutionEventBase(JsonModel):
    """Base class for execution events, containing common attributes such as action."""

    action: str | None = None
    """The user-defined action that initiated the event."""

    triggered_at: datetime | None = None
    """The time the event was triggered."""

    triggered_by: str | None = None
    """The user who triggered the event."""


class NotebookExecutionEvent(ExecutionEventBase):
    """Represents an execution event that was triggered by a notebook execution."""

    type: Literal["NOTEBOOK"] = Field(default="NOTEBOOK")
    """Represents an execution event triggered by a notebook."""

    execution_id: str | None = None
    """Includes the type identifier and the execution ID."""


class JobExecutionEvent(ExecutionEventBase):
    """A concrete execution event that represents an event triggered by a job."""

    type: Literal["JOB"] = Field(default="JOB")
    """Represents an execution event triggered by a job."""

    job_ids: List[str] | None = None
    """Includes the type identifier and a list of job IDs."""


class ManualExecutionEvent(ExecutionEventBase):
    """A concrete execution event that represents an event triggered manually."""

    type: Literal["MANUAL"] = Field(default="MANUAL")
    """Represents an execution event triggered manually. Includes only the type identifier."""


ExecutionEvent = Annotated[
    NotebookExecutionEvent | ManualExecutionEvent | JobExecutionEvent,
    Field(discriminator="type"),
]
