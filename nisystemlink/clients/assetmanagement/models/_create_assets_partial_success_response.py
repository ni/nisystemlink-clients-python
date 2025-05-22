from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset import Asset
from ._create_asset_request import CreateAssetRequest


class CreateAssetsPartialSuccessResponse(JsonModel):
    """Model for create Assets Partial Success Response."""

    assets: Optional[List[Asset]] = None
    """Gets or sets array of created assets."""

    failed: Optional[List[CreateAssetRequest]] = None
    """Gets or sets array of assets create requests that failed."""

    error: Optional[ApiError] = None
    """Gets or sets error if the create operation failed."""
