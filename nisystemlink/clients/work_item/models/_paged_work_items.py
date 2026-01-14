from typing import List

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._work_item import WorkItem


class PagedWorkItems(WithPaging):
    """The response containing the list of work items, total count and continuation token."""

    work_items: List[WorkItem]
    """A list of all the work items in this page."""

    total_count: int | None = None
    """The total number of work items that match the query."""
