from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.product.models._product import Product
from nisystemlink.clients.product.models._product_request import CreateProductRequest


class CreateProductsPartialSuccess(JsonModel):
    products: List[Product]
    """The list of products that were successfully created."""

    failed: Optional[List[CreateProductRequest]]
    """The list of products that were not created.

    If this is `None`, then all products were successfully created.
    """

    error: Optional[ApiError]
    """Error messages for products that were not created.

    If this is `None`, then all products were successfully created.
    """
