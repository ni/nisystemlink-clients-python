from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class RemoveSystemsResponse(JsonModel):
    """Model for remove systems response containing the IDs of the systems which were deleted."""

    jid: str | None = None
    """The job ID of the remove systems operation."""

    removed_ids: List[str] | None = None
    """The IDs of the systems that were successfully removed."""

    failed_ids: List[str] | None = None
    """The IDs of the systems that could not be removed."""
