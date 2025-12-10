from typing import List

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._test_plan import TestPlan


class PagedTestPlans(WithPaging):
    """The response containing the list of products, total count of products and the continuation
    token if applicable.
    """

    test_plans: List[TestPlan]
    """A list of all the products in this page."""

    total_count: int | None = None
    """The total number of products that match the query."""
