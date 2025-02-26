from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteResultsPartialSuccess(JsonModel):
    """The result of deleting multiple results when one or more results could not be deleted."""

    ids: List[str]
    """The IDs of the results that were successfully deleted."""

    failed: Optional[List[str]]
    """The IDs of the results that could not be deleted."""

    error: Optional[ApiError]
    """The error that occurred when deleting the results."""
