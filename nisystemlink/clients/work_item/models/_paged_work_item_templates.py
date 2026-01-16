from typing import List

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._work_item_template import WorkItemTemplate


class PagedWorkItemTemplates(WithPaging):
    """The response containing the list of work item templates, total count and continuation token."""

    work_item_templates: List[WorkItemTemplate]
    """A list of all the work item templates in this page."""

    total_count: int | None = None
    """The total number of work item templates that match the query."""
