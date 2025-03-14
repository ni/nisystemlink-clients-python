from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ExecutionSortField(str, Enum):
    """Possible fields used to sort executions."""

    NOTEBOOK_ID = "NOTEBOOK_ID"

    EXECUTION_HASH = "EXECUTION_HASH"

    TIMEOUT = "TIMEOUT"

    QUEUED_AT = "QUEUED_AT"

    STARTED_AT = "STARTED_AT"

    COMPLETED_AT = "COMPLETED_AT"

    STATUS = "STATUS"


class ExecutionField(str, Enum):
    """Possible fields in executions."""

    ID = "id"

    NOTEBOOK_ID = "notebookId"

    ORGANIZATION_ID = "orgId"

    USER_ID = "userId"

    PARAMETERS = "parameters"

    WORKSPACE_ID = "workspaceId"

    TIMEOUT = "timeout"

    STATUS = "status"

    QUEUED_AT = "queuedAt"

    STARTED_AT = "startedAt"

    COMPLETED_AT = "completedAt"

    LAST_UPDATED_AT = "lastUpdatedTimestamp"

    EXCEPTION = "exception"

    ERROR_CODE = "errorCode"

    REPORT_ID = "reportId"

    REPORT_SETTINGS = "reportSettings"

    RESULT = "result"

    SOURCE = "source"

    PRIORITY = "priority"

    RESOURCE_PROFILE = "resourceProfile"


class QueryExecutionsRequest(JsonModel):
    """Query for executions of Jupyter notebooks."""

    filter: Optional[str] = None
    """The query filter in Dynamic LINQ."""

    order_by: Optional[ExecutionSortField] = None
    """Possible fields used to sort executions."""

    descending: bool = False
    """Whether to return the executions in descending order."""

    projection: List[ExecutionField] = []
    """The projection to be applied for the items in the provider."""


class _QueryExecutionsRequest(JsonModel):
    """Query for executions of Jupyter notebooks."""

    filter: Optional[str] = None
    """The query filter in Dynamic LINQ."""

    order_by: Optional[ExecutionSortField] = None
    """Possible fields used to sort executions."""

    descending: bool = False
    """Whether to return the executions in descending order."""

    projection: Optional[str] = None
    """The projection to be applied for the items in the provider."""
