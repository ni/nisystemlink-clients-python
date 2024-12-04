from typing import Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class CancelJobResponse(JsonModel):
    """Model for response of a cancel job request."""

    error: ApiError
    """Represents the standard error structure."""
