from typing import List

from nisystemlink.clients.core._uplink._with_paging import WithPaging
from nisystemlink.clients.testmonitor.models import Result


class PagedResults(WithPaging):
    """The response for a Results query containing matched results."""

    results: List[Result]
    """A list of all the results in this page."""

    total_count: int | None = None
    """The total number of results that match the query."""
