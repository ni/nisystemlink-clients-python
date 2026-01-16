from typing import Annotated, Any, Dict, List, Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class Job(JsonModel):
    """Defines a job to be executed by a work item job execution."""

    functions: List[str]
    """List of function names to execute."""

    arguments: List[List[Any]]
    """List of argument lists for each function."""

    metadata: Dict[str, Any]
    """Additional metadata for the job."""


class NotebookExecution(JsonModel):
    """Defines a notebook execution for a work item."""

    action: str
    """User defined action to perform in workflow."""

    type: Literal["NOTEBOOK"] = Field(default="NOTEBOOK")
    """Type of execution, default is 'NOTEBOOK'."""

    notebookId: str
    """ID of the notebook to execute."""

    parameters: Dict[str, str] | None = None
    """	Dictionary of parameters that will be passed to the notebook when the execution is run."""


class ManualExecution(JsonModel):
    """Defines a manual execution for a work item."""

    action: str
    """User defined action to perform in workflow."""

    type: Literal["MANUAL"] = Field(default="MANUAL")
    """Type of execution, default is 'MANUAL'."""


class JobExecution(JsonModel):
    """Defines a job execution for a work item."""

    action: str
    """User defined action to perform in workflow."""

    type: Literal["JOB"] = Field(default="JOB")
    """Type of execution, default is 'JOB'."""

    jobs: List[Job] | None = None
    """List of jobs to execute."""

    systemId: str | None = None
    """Optional system ID where jobs will run."""


class NoneExecution(JsonModel):
    """Defines an unimplemented execution for a work item."""

    action: str
    """User defined action to perform in workflow."""

    type: Literal["NONE"] = Field(default="NONE")
    """Type of execution, default is 'NONE'."""


ExecutionDefinition = Annotated[
    NotebookExecution | ManualExecution | JobExecution | NoneExecution,
    Field(discriminator="type"),
]
