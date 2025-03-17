from typing import Any, Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._execution import (
    Execution,
    ExecutionErrorCode,
    ExecutionPriority,
    ExecutionResourceProfile,
    ExecutionStatus,
    ReportSettings,
)


class QueryExecutionResponse(Execution):
    """Information about an execution of a Jupyter notebook that has the cachedResult field added."""
