"""Model for start utilization request."""

from datetime import datetime
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset_identification import AssetIdentification


class StartUtilizationRequest(JsonModel):
    """Request model for starting asset utilization tracking."""

    utilization_identifier: str | None = None
    """String representing the unique identifier of an asset utilization history record."""

    minion_id: str | None = None
    """Identifier of the minion where the utilized assets are located."""

    asset_identifications: List[AssetIdentification] | None = None
    """Array of the identification information for the assets which are utilized.
    The maximum number of asset identifications allowed per request is 100."""

    utilization_category: str | None = None
    """String representing the utilization category."""

    task_name: str | None = None
    """String representing the name of the task."""

    user_name: str | None = None
    """String representing the name of the operator who utilized the asset."""

    utilization_timestamp: datetime | None = None
    """A date time value which can be used to specify the start of an utilization."""
