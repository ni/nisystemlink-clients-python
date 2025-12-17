"""Model for update utilization partial success response."""

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class UpdateUtilizationPartialSuccessResponse(JsonModel):
    """Response model for update utilization operation with partial success support."""

    error: ApiError | None = None
    """Error information if any failures occurred."""

    updated_utilization_ids: list[str] | None = None
    """Array of utilization identifiers for the entries that were updated."""

    failed: list[str] | None = None
    """Array of utilization identifiers for the entries that failed to update."""
