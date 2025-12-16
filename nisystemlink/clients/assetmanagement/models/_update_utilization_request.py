"""Model for updating utilization (heartbeat or end)."""

from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class UpdateUtilizationRequest(JsonModel):
    """Request model for updating utilization (heartbeat or end)."""

    utilization_identifiers: Optional[List[str]] = None
    """Array representing the unique identifier of an asset utilization history record."""

    utilization_timestamp: Optional[datetime] = None
    """A date time value which can be used to specify the heartbeat timestamp."""
