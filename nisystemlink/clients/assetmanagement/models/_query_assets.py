from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class OrderBy(Enum):
    """Field by which assets can be ordered/sorted. If OrderBy is not specified, no sorting will applied."""

    LAST_UPDATED_TIMESTAMP = "LAST_UPDATED_TIMESTAMP"


class QueryAssetRequest(JsonModel):
    """Model for object containing filters to apply when retrieving assets."""

    ids: Optional[List[str]] = None
    """Gets or sets identifiers of the assets to be retrieved."""

    skip: int
    """Gets or sets the number of resources to skip in the result when paging."""

    take: int
    """Gets or sets how many resources to return in the result, or -1 to use a default defined by the service."""

    order_by: Optional[OrderBy] = None
    """Field by which assets can be ordered/sorted. If OrderBy is not specified, no sorting will applied."""

    descending: bool
    """Whether to return the assets in the descending order. If OrderBy is not specified, this property is ignored."""

    calibratable_only: bool
    """Gets or sets whether to generate a report with calibrated asset specific columns:"""

    filter: Optional[str] = None
    """Gets or sets the filter criteria for assets. Consists of a string of queries composed using AND/OR operators."""
