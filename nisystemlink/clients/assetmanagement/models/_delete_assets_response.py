from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteAssetsResponse(JsonModel):
    """Model for delete Assets Response containing the ids of the assets which were deleted"""

    ids: List[str] | None = None
    """Gets or sets array of asset identifiers which were deleted."""

    failed: List[str] | None = None
    """Gets or sets array of asset identifiers that failed to delete."""

    error: ApiError | None = None
    """Gets or sets error if the delete operation failed."""
