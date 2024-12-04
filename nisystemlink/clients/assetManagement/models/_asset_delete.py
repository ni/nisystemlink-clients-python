from typing import List, Optional
from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

class DeleteAssetsRequest(JsonModel):
    """Model for request body containing IDs of the assets to delete all information for."""

    ids: Optional[List[str]] = None
    """Gets or sets multiple asset IDs for which to delete all data. The maximum number of asset IDs allowed per request is 1000."""

class DeleteAssetsResponse(JsonModel):
    """Model for delete Assets Response containing the ids of the assets which were deleted, the ids of the assets which failed to be deleted and any errors encountered."""

    error: Optional[ApiError] = None

    ids: Optional[List[str]] = None
    "Gets or sets array of asset identifiers which were deleted."

    failed: Optional[List[str]] = None
    """Gets or sets array of asset identifiers that failed to delete."""