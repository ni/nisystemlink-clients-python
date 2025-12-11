from datetime import datetime
from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AssetUtilizationHistoryItem(JsonModel):
    """Model representing an asset utilization history record."""

    utilization_identifier: Optional[str] = None
    """Gets or sets string representing the unique identifier of an asset utilization history record."""

    asset_identifier: Optional[str] = None
    """Gets or sets string representing the unique identifier of an asset."""

    minion_id: Optional[str] = None
    """Gets or sets identifier of the minion where the asset is located."""

    category: Optional[str] = None
    """Gets or sets string representing the utilization task category."""

    task_name: Optional[str] = None
    """Gets or sets string representing the name of the task."""

    user_name: Optional[str] = None
    """Gets or sets string representing the name of the operator who utilized the asset."""

    start_timestamp: Optional[datetime] = None
    """Gets or sets a date time value which can be used to specify the start of an utilization."""

    end_timestamp: Optional[datetime] = None
    """Gets or sets a date time value which can be used to specify the end of an utilization."""

    heartbeat_timestamp: Optional[datetime] = None
    """Gets or sets a date time value which can be used to specify the heartbeat of an utilization."""
