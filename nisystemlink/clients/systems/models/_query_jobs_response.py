from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._http_error import HttpError


class QueryJobsResponse(JsonModel):
    """Model for response of a query request."""

    error: Optional[HttpError] = None
    """Represents the standard error structure."""

    data: Optional[List[str]] = None
    """The data returned by the query."""

    count: Optional[int] = None
    """The total number of resources that matched the query."""
