from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset import Asset
from ._create_asset_request import CreateAssetRequest


class CreateAssetsPartialSuccessResponse(JsonModel):
    """Model for create Assets Partial Success Response."""

    assets: List[Asset] | None = None
    """Gets or sets array of created assets."""

    failed: List[CreateAssetRequest] | None = None
    """Gets or sets array of assets create requests that failed."""

    error: ApiError | None = None
    """Gets or sets error if the create operation failed."""
