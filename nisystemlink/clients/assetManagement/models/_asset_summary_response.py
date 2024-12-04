from typing import Optional
from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

class AssetSummaryResponse(JsonModel):
    """Model for asset summary response containing the total number of assets, the number of assets which are active, i.e. present in a connected system, and the number of assets which are not active."""

    error: Optional[ApiError] = None

    active: int
    """Gets or sets number of assets which are active, i.e. present in a connected system."""

    not_active: int
    """Gets or sets number of assets which are not active."""

    total: int
    """Gets or sets total number of managed assets."""

    in_use: Optional[int] = None
    """Gets or sets total number of used assets."""

    not_in_use: Optional[int] = None
    """Gets or sets total number of unused assets."""

    with_alarms: Optional[int] = None
    """Gets or sets total number of assets with alarms"""

    approaching_recommended_due_date: int
    """Gets or sets number of assets approaching calibration date."""

    past_recommended_due_date: int
    """Gets or sets number of assets past their calibration date."""

    total_calibrated: Optional[int] = None
    """Gets or sets total number of assets supporting calibration."""

    out_for_calibration: int
    """Gets or sets total number of assets out of calibration."""