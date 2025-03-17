from typing import Any, Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._execution import (
    ExecutionErrorCode,
    ExecutionPriority,
    ExecutionResourceProfile,
    ExecutionStatus,
    ReportSettings,
)


class QueryExecutionResponse(JsonModel):
    """Information about an execution of a Jupyter notebook that has the cachedResult field added."""

    id: Optional[str] = None
    """The ID of the execution."""

    notebook_id: Optional[str] = None
    """The ID of the executed notebook."""

    organization_id: Optional[str] = Field(None, alias="orgId")
    """The org ID of the user creating the request."""

    user_id: Optional[str] = None
    """The user ID of the user creating the request."""

    parameters: Optional[Dict[str, Any]] = None
    """The input parameters for this execution of the notebook. The keys are strings and the values can be of any
    valid JSON type."""

    workspace_id: Optional[str] = None
    """The ID of the workspace this execution belongs to."""

    timeout: Optional[int] = None
    """The number of seconds the execution runs before it aborts if uncompleted. The timer starts once status
    is IN_PROGRESS. 0 means infinite."""

    status: Optional[ExecutionStatus] = None
    """Status of an execution."""

    queued_at: Optional[str] = None
    """Timestamp of when the notebook execution was queued."""

    started_at: Optional[str] = None
    """Timestamp of when the notebook execution was started."""

    completed_at: Optional[str] = None
    """Timestamp of when the notebook execution was completed."""

    last_updated_timestamp: Optional[str] = None
    """Timestamp of when the notebook execution was last updated."""

    exception: Optional[str] = None
    """Exception that occurred during the execution. This is used only when status is FAILED."""

    error_code: Optional[ExecutionErrorCode] = None
    """Execution error code."""

    report_id: Optional[str] = None
    """The ID of the report this execution generates."""

    report_settings: Optional[ReportSettings] = None
    """Settings of the Report"""

    result: Optional[Dict[str, Optional[str]]] = None
    """Result of the execution. This is used only when status is SUCCEEDED."""

    priority: Optional[ExecutionPriority] = None
    """Execution priority. Can be one of Low, Medium or High."""

    resource_profile: Optional[ExecutionResourceProfile] = None
