from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class LinkFilesPartialSuccessResponse(JsonModel):
    """Model for link files Partial Success Response."""

    error: Optional[ApiError] = None

    succeeded: Optional[List[str]] = None
    """The file ids which were successfully linked."""

    failed: Optional[List[str]] = None
    """The file ids which failed to link."""
