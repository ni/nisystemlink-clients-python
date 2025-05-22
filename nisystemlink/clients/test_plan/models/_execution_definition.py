from typing import Annotated, Any, List, Literal, Optional, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class Job(JsonModel):
    """Represents a job to be executed, including its functions, arguments, and metadata."""

    functions: List[str]
    """List of function names to execute."""

    arguments: List[List[Any]]
    """List of argument lists for each function."""

    metadata: dict[str, Any]
    """Additional metadata for the job."""


class NotebookExecution(JsonModel):
    """Defines the execution of a notebook."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["NOTEBOOK"] = Field(default="NOTEBOOK")
    """Type of execution, default is 'NOTEBOOK'."""

    notebookId: str
    """ID of the notebook to execute."""


class ManualExecution(JsonModel):
    """Represents a manual execution definition."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["MANUAL"] = Field(default="MANUAL")
    """Type of execution, default is 'MANUAL'."""


class JobExecution(JsonModel):
    """Defines the execution of one or more jobs."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["JOB"] = Field(default="JOB")
    """Type of execution, default is 'JOB'."""

    jobs: List[Job]
    """List of jobs to execute."""

    systemId: Optional[str] = None
    """Optional system ID where jobs will run."""


class ScheduleExecution(JsonModel):
    """Represents a scheduled execution definition."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["SCHEDULE"] = Field(default="SCHEDULE")
    """Type of execution, default is 'SCHEDULE'."""


class UnscheduleExecution(JsonModel):
    """Represents an unscheduled execution definition."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["UNSCHEDULE"] = Field(default="UNSCHEDULE")
    """Type of execution, default is 'UNSCHEDULE'."""


class NoneExecution(JsonModel):
    """Represents a definition where no execution is specified."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["None"] = Field(default="None")
    """Type of execution, default is 'None'."""


ExecutionDefinition = Annotated[
    Union[
        NotebookExecution,
        ManualExecution,
        JobExecution,
        ScheduleExecution,
        UnscheduleExecution,
        NoneExecution,
    ],
    Field(discriminator="type"),
]
