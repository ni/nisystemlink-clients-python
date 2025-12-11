"""Model for start utilization partial success response."""

from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset_identification_model import AssetIdentificationModel


class StartUtilizationPartialSuccessResponse(JsonModel):
    """Response model for start utilization operation with partial success support."""

    error: Optional[ApiError] = None
    """Error information if any failures occurred."""

    assets_with_started_utilization: Optional[List[AssetIdentificationModel]] = None
    """Array containing the asset identification data for the assets that started being utilized."""

    failed: Optional[List[AssetIdentificationModel]] = None
    """Array containing the asset identification data for the assets that failed to start being utilized."""
