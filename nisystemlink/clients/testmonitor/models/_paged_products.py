from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging
from nisystemlink.clients.testmonitor.models import Product


class PagedProducts(WithPaging):
    """The response for a Products query containing matched products."""

    products: List[Product]
    """A list of all the products in this page."""

    total_count: Optional[int]
    """The total number of products that match the query."""
