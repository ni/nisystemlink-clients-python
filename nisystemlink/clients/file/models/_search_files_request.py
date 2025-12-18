from nisystemlink.clients.core._uplink._json_model import JsonModel


class SearchFilesRequest(JsonModel):
    """Request model for searching files."""

    filter: str | None = None
    """
    Filter string for searching files.
    """

    skip: int | None = None
    """
    How many files to skip in the result when paging.
    """

    take: int | None = None
    """
    How many files to return in the result.
    """

    order_by: str | None = None
    """
    The name of the metadata field to sort by.
    """

    order_by_descending: bool | None = False
    """
    Whether to sort in descending order.
    """
