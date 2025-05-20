from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.systems.models._systems import System


class QuerySystemsResponse(JsonModel):
    """Model for query systems request."""

    count: Optional[int] = None
    """Number of systems match the query."""

    data: Optional[List[System | object]] = None
    """Contains info of the queried systems."""
