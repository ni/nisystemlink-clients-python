from typing import List

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.product.models._product import Product
from nisystemlink.clients.product.models._product_request import CreateProductRequest


class CreateProductsPartialSuccess(JsonModel):
    products: List[Product]
    """The list of products that were successfully created."""

    failed: List[CreateProductRequest] | None = None
    """The list of products that were not created.

    If this is `None`, then all products were successfully created.
    """

    error: ApiError | None = None
    """Error messages for products that were not created.

    If this is `None`, then all products were successfully created.
    """
