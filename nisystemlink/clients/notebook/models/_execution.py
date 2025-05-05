from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class SourceType(str, Enum):
    """Source type of an execution"""

    MANUAL = "MANUAL"

    TRIGGERED = "TRIGGERED"


class Source(JsonModel):
    """An object that defines properties set by routine service"""

    type: SourceType
    """Source type of an execution"""

    routine_id: Optional[str] = None
    """ID of the routine that triggered the execution"""

    event_id: Optional[str] = None
    """Unique identifier of event that triggered the execution"""


class ReportType(str, Enum):
    """Available types for a report that is going to be generated."""

    NO_REPORT = "NO_REPORT"

    HTML = "HTML"

    PDF = "PDF"


class ReportSettings(JsonModel):
    """A class that defines settings of the Report"""

    format: ReportType
    """Type for the report that is going to be generated."""

    exclude_code: bool
    """Boolean parameter that will define if the source code should be included in the report or not."""


class ExecutionPriority(str, Enum):
    """Execution priority. Can be one of Low, Medium or High."""

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"


class ExecutionResourceProfile(str, Enum):

    DEFAULT = "DEFAULT"

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"


class ExecutionStatus(str, Enum):
    """Status of an execution."""

    IN_PROGRESS = "IN_PROGRESS"

    QUEUED = "QUEUED"

    FAILED = "FAILED"

    SUCCEEDED = "SUCCEEDED"

    CANCELED = "CANCELED"

    TIMED_OUT = "TIMED_OUT"


class ExecutionErrorCode(str, Enum):
    """Execution error code."""

    NO_ERROR = "NO_ERROR"

    NOTEBOOK_ERROR = "NOTEBOOK_ERROR"

    NOTEBOOK_TIMEOUT_ERROR = "NOTEBOOK_TIMEOUT_ERROR"

    NOTEBOOK_NOT_FOUND_ERROR = "NOTEBOOK_NOT_FOUND_ERROR"

    NOTEBOOK_RESULT_TOO_BIG_ERROR = "NOTEBOOK_RESULT_TOO_BIG_ERROR"

    NOT_PUBLISHED_ERROR = "NOT_PUBLISHED_ERROR"

    OUT_OF_MEMORY_ERROR = "OUT_OF_MEMORY_ERROR"

    UNKNOWN_ERROR = "UNKNOWN_ERROR"

    DEAD_KERNEL_ERROR = "DEAD_KERNEL_ERROR"

    EXECUTION_COULD_NOT_BE_RETRIED = "EXECUTION_COULD_NOT_BE_RETRIED"


class Execution(JsonModel):
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
    """The number of seconds the execution runs before it aborts if uncompleted. The timer starts once status is
    IN_PROGRESS. 0 means infinite."""

    status: Optional[ExecutionStatus] = None
    """Status of an execution."""

    queued_at: Optional[datetime] = None
    """Timestamp of when the notebook execution was queued."""

    started_at: Optional[datetime] = None
    """Timestamp of when the notebook execution was started."""

    completed_at: Optional[datetime] = None
    """Timestamp of when the notebook execution was completed."""

    last_updated_timestamp: Optional[datetime] = None
    """Timestamp of when the notebook execution was last updated."""

    last_updated_by: Optional[str] = None
    """"The user ID of the user who last updated the execution."""

    retry_count: Optional[int] = None
    """The number of manually retried attempts of the notebook execution."""

    exception: Optional[str] = None
    """Exception that occured during the execution. This is used only when status is FAILED."""

    error_code: Optional[ExecutionErrorCode] = None
    """Execution error code."""

    report_id: Optional[str] = None
    """The ID of the report this execution generates."""

    report_settings: Optional[ReportSettings] = None
    """Settings of the Report"""

    result: Optional[Dict[str, Optional[object]]] = None
    """Result of the execution. This is used only when status is SUCCEEDED."""

    source: Optional[Source] = None
    """An object that defines properties set by routine service"""

    priority: Optional[ExecutionPriority] = None
    """Execution priority. Can be one of Low, Medium or High."""

    resource_profile: Optional[ExecutionResourceProfile] = None
    """Resource profile of the execution."""
