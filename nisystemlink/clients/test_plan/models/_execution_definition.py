from typing import List, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel
class Job(JsonModel):
    """Represents a job to be executed, including its functions, arguments, and metadata."""

    functions: List[str]
    """List of function names to execute."""

    arguments: List[List[object]]
    """List of argument lists for each function."""

    metadata: dict[str, object]
    """Additional metadata for the job."""

class NotebookExecution(JsonModel):
    """Defines the execution of a notebook."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: str = 'NOTEBOOK'
    """Type of execution, default is 'NOTEBOOK'."""

    notebookId: str
    """ID of the notebook to execute."""


class ManualExecution(JsonModel):
    """Represents a manual execution definition."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: str = 'MANUAL'
    """Type of execution, default is 'MANUAL'."""

class JobExecution(JsonModel):
    """Defines the execution of one or more jobs."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: str = 'JOB'
    """Type of execution, default is 'JOB'."""

    jobs: List[Job]
    """List of jobs to execute."""

    systemId: str | None = None
    """Optional system ID where jobs will run."""


class ScheduleExecution(JsonModel):
    """Represents a scheduled execution definition."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: str = 'SCHEDULE'
    """Type of execution, default is 'SCHEDULE'."""


class UnscheduleExecution(JsonModel):
    """Represents an unscheduled execution definition."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: str = 'UNSCHEDULE'
    """Type of execution, default is 'UNSCHEDULE'."""

class NoneExecution(JsonModel):
    """Represents a definition where no execution is specified."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: str = 'None'
    """Type of execution, default is 'None'."""

ExecutionDefinition = Union[
    NotebookExecution,
    ManualExecution,
    JobExecution,
    NoneExecution,
    ScheduleExecution,
    UnscheduleExecution
]