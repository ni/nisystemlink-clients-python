from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset import Asset


class QueryAssetsResponse(JsonModel):
    """Model for assets Response containing the assets satisfying the query and the total count of matching assets."""

    assets: List[Asset] | None = None
    """Gets or sets array of assets."""

    total_count: int | None = None
    """Gets or sets the total number of Assets which match the query."""
