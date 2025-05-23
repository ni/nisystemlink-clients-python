from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class Job(JsonModel):
    """Represents a job to be executed, including its functions, arguments, and metadata."""

    functions: List[str]
    """List of function names to execute."""

    arguments: List[List[Any]]
    """List of argument lists for each function."""

    metadata: Dict[str, Any]
    """Additional metadata for the job."""


class NotebookExecution(JsonModel):
    """Defines the execution of a notebook."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["NOTEBOOK"] = Field(default="NOTEBOOK")
    """Type of execution, default is 'NOTEBOOK'."""

    notebookId: str
    """ID of the notebook to execute."""

    parameters: Optional[Dict[str, str]] = None
    """	Dictionary of parameters that will be passed to the notebook when the execution is run."""


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

    jobs: Optional[List[Job]] = None
    """List of jobs to execute."""

    systemId: Optional[str] = None
    """Optional system ID where jobs will run."""


class NoneExecution(JsonModel):
    """Represents a definition where no execution is specified."""

    action: str
    """User defined action to perform in workflow (user defined)."""

    type: Literal["NONE"] = Field(default="NONE")
    """Type of execution, default is 'NONE'."""


ExecutionDefinition = Annotated[
    Union[
        NotebookExecution,
        ManualExecution,
        JobExecution,
        NoneExecution,
    ],
    Field(discriminator="type"),
]
