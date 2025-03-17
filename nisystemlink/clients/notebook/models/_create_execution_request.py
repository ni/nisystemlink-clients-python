from typing import Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._execution import (
    ExecutionPriority,
    ExecutionResourceProfile,
    ReportSettings,
)


class CreateExecutionRequest(JsonModel):
    """Creation information about an execution of a Jupyter notebook."""

    notebook_id: str = Field(..., min_length=1)
    """The ID of the notebook to execute."""

    parameters: Optional[Dict[str, Optional[str]]] = None
    """The input parameters for this execution of the notebook. The keys are strings and the values can be of any
    valid JSON type."""

    workspace_id: str = Field(..., min_length=1)
    """The ID of the workspace this execution belongs to."""

    timeout: Optional[int] = None
    """The number of seconds the execution runs before it aborts if uncompleted. The timer starts once status
    is IN_PROGRESS. 0 means infinite."""

    result_cache_period: Optional[int] = None
    """The period of time, in seconds, when the result of a previous notebook execution can be used as the
    result of the current notebook execution. Results will only be reused if the notebook and input parameters match.
    A value of 0 means do not reuse results from any previous executions. A value of -1 means always reuse results if
    possible and return an error if not possible. This prevents actual execution of a notebook."""

    report_settings: Optional[ReportSettings] = None
    """Settings of the Report"""

    client_requests_id: Optional[str] = None
    """The client request ID unique for each execution to be created. This is provided by the caller to be able
    to track executions that could not be created. The error response will contain this in the resourceId field.
    If not provided, the notebookId is used as the resourceId."""

    priority: Optional[ExecutionPriority] = None
    """Execution priority. Can be one of Low, Medium or High."""

    resource_profile: Optional[ExecutionResourceProfile] = None
    """Resource profile of the execution."""
