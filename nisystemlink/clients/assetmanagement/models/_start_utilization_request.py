"""Model for start utilization request."""

from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset_identification_model import AssetIdentificationModel


class StartUtilizationRequest(JsonModel):
    """Request model for starting asset utilization tracking."""

    utilization_identifier: Optional[str] = None
    """String representing the unique identifier of an asset utilization history record."""

    minion_id: Optional[str] = None
    """Identifier of the minion where the utilized assets are located."""

    asset_identifications: Optional[List[AssetIdentificationModel]] = None
    """Array of the identification information for the assets which are utilized.
    The maximum number of asset identifications allowed per request is 100."""

    utilization_category: Optional[str] = None
    """String representing the utilization category."""

    task_name: Optional[str] = None
    """String representing the name of the task."""

    user_name: Optional[str] = None
    """String representing the name of the operator who utilized the asset."""

    utilization_timestamp: Optional[datetime] = None
    """A date time value which can be used to specify the start of an utilization.
    This parameter must have the "ISO 8601" format in order to be considered valid."""
