from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset import Asset


class AssetsResponse(JsonModel):
    """Model for assets Response containing the assets satisfying the query and the total count of matching assets."""

    assets: Optional[List[Asset]] = None
    """Gets or sets array of assets."""

    total_count: int
    """Gets or sets the total number of Assets which match the query."""
