from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError


class LinkFilesPartialSuccessResponse:
    """Model for a Link Files Partial Success Response."""

    succeeded: Optional[List[str]] = None
    """Gets or sets array of file IDs that were successfully linked to assets."""

    failed: Optional[List[str]] = None
    """Gets or sets array of file IDs that failed to link to assets."""

    error: Optional[ApiError] = None
    """Gets or sets error if the link file operation failed."""