from typing import List

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class LinkFilesPartialSuccessResponse(JsonModel):
    """Model for a Link Files Partial Success Response."""

    succeeded: List[str] | None = None
    """Gets or sets array of file IDs that were successfully linked to assets."""

    failed: List[str] | None = None
    """Gets or sets array of file IDs that failed to link to assets."""

    error: ApiError | None = None
    """Gets or sets error if the link file operation failed."""
