from nisystemlink.clients.core._uplink._json_model import JsonModel


class BaseFileRequest(JsonModel):
    """Base class for file request models containing common query parameters."""

    skip: int | None = None
    """
    How many files to skip in the result when paging.
    """

    take: int | None = None
    """
    How many files to return in the result.
    """

    order_by_descending: bool | None = False
    """
    Whether to sort in descending order.
    """
