from enum import Enum
from typing import Optional, Union, List
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
    """Possible fields used to sort executions."""

    ID = "id"

    NOTEBOOK_ID = "notebook_id"

    ORGANIZATION_ID = "org_id"

    USER_ID = "user_id"

    PARAMETERS = "parameters"

    WORKSPACE_ID = "workspace_id"

    TIMEOUT = "timeout"

    STATUS = "status"

    QUEUED_AT = "queued_at"

    STARTED_AT = "started_at"

    COMPLETED_AT = "completed_at"

    LAST_UPDATED_AT = "last_updated_at"

    EXECUTION = "execution"

    ERROR_CODE = "error_code"

    REPORT_ID = "report_id"

    REPORT_SETTINGS = "report_settings"

    RESULT = "result"

    SOURCE = "source"

    PRIORITY = "priority"

    RESOURCE_PROFILE = "resource_profile"


class QueryExecutions(JsonModel):
    """Query for executions of Jupyter notebooks."""

    filter: Optional[str] = None
    """The query filter in Dynamic LINQ."""

    order_by: ExecutionSortField
    """Possible fields used to sort executions."""

    descending: bool = False
    """Whether to return the executions in descending order."""

    projection: List[Union[ExecutionField, str]] = []
    """The projection to be applied for the items in the provider."""


class _QueryExecutions(JsonModel):
    """Query for executions of Jupyter notebooks."""

    filter: Optional[str] = None
    """The query filter in Dynamic LINQ."""

    order_by: ExecutionSortField
    """Possible fields used to sort executions."""

    descending: bool = False
    """Whether to return the executions in descending order."""

    projection: Optional[str] = None
    """The projection to be applied for the items in the provider."""
