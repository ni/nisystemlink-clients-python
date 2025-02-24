from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging
from nisystemlink.clients.product.models import Product
from nisystemlink.clients.product.models._query_products_response import (
    QueryProductsResponse,
)


class PagedProducts(WithPaging):
    """The response containing the list of products, total count of products and the continuation
    token if applicable.
    """

    products: List[Product]
    """A list of all the products in this page."""

    total_count: Optional[int]
    """The total number of products that match the query."""


class PagedQueryProductsResponse(WithPaging):
    """The response for a Products query containing matched products.

    The response fields are all optional and are based on the projection if given.
    """

    products: List[QueryProductsResponse]
    """A list of all the products in this page."""

    total_count: Optional[int]
    """The total number of products that match the query."""
