from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteProductsPartialSuccess(JsonModel):
    """The result of deleting multiple products when one or more products could not be deleted."""

    ids: List[str]
    """The IDs of the products that were successfully deleted."""

    failed: Optional[List[str]]
    """The IDs of the products that could not be deleted."""

    error: Optional[ApiError]
    """The error that occurred when deleting the products."""
