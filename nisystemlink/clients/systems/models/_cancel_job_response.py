from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._http_error import HttpError


class CancelJobResponse(JsonModel):
    """Model for response of a cancel job request."""

    error: Optional[HttpError] = None
    """Represents the standard error structure."""
