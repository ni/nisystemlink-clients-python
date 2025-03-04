from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging
from nisystemlink.clients.product.models._product import Product


class PagedProducts(WithPaging):
    """The response containing the list of products, total count of products and the continuation
    token if applicable.
    """

    products: List[Product]
    """A list of all the products in this page."""

    total_count: Optional[int]
    """The total number of products that match the query."""
