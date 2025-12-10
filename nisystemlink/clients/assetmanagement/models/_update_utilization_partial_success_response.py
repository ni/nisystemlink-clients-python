"""Model for update utilization partial success response."""

from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class UpdateUtilizationPartialSuccessResponse(JsonModel):
    """Response model for update utilization operation with partial success support."""

    error: Optional[ApiError] = None
    """Error information if any failures occurred."""

    updated_utilization_ids: Optional[List[str]] = None
    """Array of utilization identifiers for the entries that were updated."""

    failed: Optional[List[str]] = None
    """Array of utilization identifiers for the entries that failed to update."""
