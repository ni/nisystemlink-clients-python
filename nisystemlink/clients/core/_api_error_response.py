from nisystemlink.clients.core._api_error import ApiError


class ApiErrorResponse:
    """Represents an error response from the SystemLink API responses."""

    error: ApiError
