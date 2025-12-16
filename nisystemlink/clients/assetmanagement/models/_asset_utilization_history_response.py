from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._asset_utilization_history_item import AssetUtilizationHistoryItem


class AssetUtilizationHistoryResponse(WithPaging):
    """Response model for asset utilization history query."""

    asset_utilizations: list[AssetUtilizationHistoryItem] | None = None
    """Array of asset utilizations."""
