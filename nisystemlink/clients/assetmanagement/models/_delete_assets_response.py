from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteAssetsResponse(JsonModel):
    """Model for delete Assets Response containing the ids of the assets which were deleted"""

    ids: Optional[List[str]] = None
    """Gets or sets array of asset identifiers which were deleted."""

    failed: Optional[List[str]] = None
    """Gets or sets array of asset identifiers that failed to delete."""

    error: Optional[ApiError] = None
    """Gets or sets error if the delete operation failed."""
