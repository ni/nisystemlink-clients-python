from datetime import datetime
from enum import Enum
from typing import Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging


class UtilizationOrderBy(Enum):
    """Field by which asset utilization history records can be ordered/sorted."""

    START_TIMESTAMP = "START_TIMESTAMP"


class QueryAssetUtilizationHistoryRequest(WithPaging):
    """Model for object containing filters for asset utilization and assets."""

    utilization_filter: Optional[str] = None
    """
    The filter criteria for asset utilization. Consists of a string of queries
    composed using AND/OR operators. Valid properties: MinionId, Category, UserName, TaskName,
    StartTimestamp, EndTimestamp.
    """

    asset_filter: Optional[str] = None
    """
    The filter criteria for assets. Consists of a string of queries composed
    using AND/OR operators. Valid properties include AssetIdentifier, SerialNumber, ModelName,
    VendorName, Location.MinionId, and many others.
    """

    take: Optional[int] = None
    """The maximum number of asset utilization history records to return."""

    order_by: Optional[UtilizationOrderBy] = None
    """
    The field to order results by. If not provided, default ordering is applied.
    """

    order_by_descending: Optional[bool] = None
    """Whether to return the asset utilization history records in descending order."""

    start_time: Optional[datetime] = None
    """Start of the date range. Defaults to 90 days ago."""

    end_time: Optional[datetime] = None
    """End of the date range. Defaults to current time."""
