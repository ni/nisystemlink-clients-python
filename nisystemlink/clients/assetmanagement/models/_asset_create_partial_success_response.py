from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset import Asset
from ._asset_create_request import AssetCreateRequest


class AssetsCreatePartialSuccessResponse(JsonModel):
    """Model for create Assets Partial Success Response."""

    error: Optional[ApiError] = None
    """Gets or sets error information if the request failed."""

    assets: Optional[List[Asset]] = None
    """Gets or sets array of created assets."""

    failed: Optional[List[AssetCreateRequest]] = None
    """Gets or sets array of assets create requests that failed."""
