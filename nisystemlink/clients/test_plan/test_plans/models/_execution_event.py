from typing import List, Literal, Union
from nisystemlink.clients.core._uplink._json_model import JsonModel

class ExecutionEventBase(JsonModel):
    action: str
    """Base class for execution events, containing common attributes such as action."""

    triggeredAt: str
    """the time the event was triggered."""

    triggeredBy: str = None
    """and the user who triggered it."""


class NotebookExecutionEvent(ExecutionEventBase):
    type: str = 'NOTEBOOK'
    """Represents an execution event triggered by a notebook."""

    executionId: str
    """Includes the type identifier and the execution ID."""


class JobExecutionEvent(ExecutionEventBase):
    type: str = 'JOB'
    """Represents an execution event triggered by a job."""

    jobIds: List[str]
    """Includes the type identifier and a list of job IDs."""


class ManualExecutionEvent(ExecutionEventBase):
    type: str = 'MANUAL'
    """Represents an execution event triggered manually. Includes only the type identifier."""

ExecutionEvent = Union[NotebookExecutionEvent, ManualExecutionEvent, JobExecutionEvent]
