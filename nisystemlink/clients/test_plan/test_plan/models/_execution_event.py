from typing import List, Optional, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ExecutionEventBase(JsonModel):
    """Base class for execution events, containing common attributes such as action."""

    action: Optional[str] = None
    """The user-defined action that initiated the event."""

    triggered_at: Optional[str] = None
    """The time the event was triggered."""

    triggered_by: Optional[str] = None
    """The user who triggered the event."""


class NotebookExecutionEvent(ExecutionEventBase):
    """Represents an execution event that was triggered by a notebook execution."""

    type: Optional[str] = "NOTEBOOK"
    """Represents an execution event triggered by a notebook."""

    execution_id: Optional[str] = None
    """Includes the type identifier and the execution ID."""


class JobExecutionEvent(ExecutionEventBase):
    """A concrete execution event that represents an event triggered by a job."""

    type: Optional[str] = "JOB"
    """Represents an execution event triggered by a job."""

    job_ids: Optional[List[str]]
    """Includes the type identifier and a list of job IDs."""


class ManualExecutionEvent(ExecutionEventBase):
    """A concrete execution event that represents an event triggered manually."""

    type: Optional[str] = "MANUAL"
    """Represents an execution event triggered manually. Includes only the type identifier."""


ExecutionEvent = Union[NotebookExecutionEvent, ManualExecutionEvent, JobExecutionEvent]
