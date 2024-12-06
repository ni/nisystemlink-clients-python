from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._job import Job


class QueryJobsResponse(JsonModel):
    """Model for response of a query request."""

    error: ApiError
    """Represents the standard error structure."""

    data: Optional[List[Job]] = None
    """The data returned by the query."""

    count: int
    """The total number of resources that matched the query."""
