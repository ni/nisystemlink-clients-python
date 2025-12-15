from typing import Any, Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class QuerySystemsResponse(JsonModel):
    """Model for query systems request."""

    count: int | None = None
    """Number of systems match the query."""

    data: List[Dict[str, Any]] | None = None
    """Contains info of the queried systems."""
