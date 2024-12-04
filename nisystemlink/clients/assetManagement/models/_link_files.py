from typing import List, Optional
from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

class LinkFilesRequest(JsonModel):
    """Model for the asset link files request."""

    file_ids: Optional[List[str]] = None
    """Gets or sets file IDs associated with an asset. The maximum number of file IDs allowed per request is 1000."""

class LinkFilesPartialSuccessResponse(JsonModel):
    """Model for link files Partial Success Response."""

    error: Optional[ApiError] = None

    succeeded: Optional[List[str]] = None
    """The file ids which were successfully linked."""

    failed: Optional[List[str]] = None
    """The file ids which failed to link."""