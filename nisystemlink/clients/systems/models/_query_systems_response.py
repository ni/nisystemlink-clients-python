from typing import Any, Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class QuerySystemsResponse(JsonModel):
    """Model for query systems request."""

    count: Optional[int] = None
    """Number of systems match the query."""

    data: Optional[List[Dict[str, Any]]] = None
    """Contains info of the queried systems."""
