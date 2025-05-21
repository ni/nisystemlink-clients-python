from typing import List, Optional, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ExecutionEventBase(JsonModel):
    action: Optional[str] = None
    """Base class for execution events, containing common attributes such as action."""

    triggeredAt: Optional[str] = None
    """the time the event was triggered."""

    triggeredBy: Optional[str] = None
    """and the user who triggered it."""


class NotebookExecutionEvent(ExecutionEventBase):
    type: Optional[str] = "NOTEBOOK"
    """Represents an execution event triggered by a notebook."""

    executionId: Optional[str] = None
    """Includes the type identifier and the execution ID."""


class JobExecutionEvent(ExecutionEventBase):
    type: Optional[str] = "JOB"
    """Represents an execution event triggered by a job."""

    jobIds: Optional[List[str]]
    """Includes the type identifier and a list of job IDs."""


class ManualExecutionEvent(ExecutionEventBase):
    type: Optional[str] = "MANUAL"
    """Represents an execution event triggered manually. Includes only the type identifier."""


ExecutionEvent = Union[NotebookExecutionEvent, ManualExecutionEvent, JobExecutionEvent]
