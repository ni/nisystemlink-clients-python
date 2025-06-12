from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class ApiErrorResponse(JsonModel):
    """Represents an error response from the SystemLink API responses."""

    error: ApiError
