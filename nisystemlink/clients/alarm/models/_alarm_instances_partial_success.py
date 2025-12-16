from typing import List

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class AlarmInstancesPartialSuccess(JsonModel):
    """Base class for partial success responses containing success/failure lists and error information."""

    failed: List[str]
    """The instanceIds that failed the operation."""

    error: ApiError | None = None
    """The error that occurred during the operation."""
