from typing import List

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._test_plan_templates import TestPlanTemplate


class PagedTestPlanTemplates(WithPaging):
    """The response containing the list of products, total count of products and the continuation
    token if applicable.
    """

    test_plan_templates: List[TestPlanTemplate]
    """A list of all the products in this page."""

    total_count: int | None = None
    """The total number of products that match the query."""
