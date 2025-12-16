from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class SearchFilesRequest(JsonModel):
    """Request model for searching files."""

    filter: Optional[str] = None
    """
    Filter string for searching files.
    """

    skip: Optional[int] = None
    """
    How many files to skip in the result when paging.
    """

    take: Optional[int] = None
    """
    How many files to return in the result.
    """

    order_by: Optional[str] = None
    """
    The name of the metadata field to sort by.
    """

    order_by_descending: Optional[bool] = None
    """
    Whether to sort in descending order.
    """
