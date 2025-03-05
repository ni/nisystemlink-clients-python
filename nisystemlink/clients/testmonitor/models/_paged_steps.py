from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging
from nisystemlink.clients.testmonitor.models._step import Step


class PagedSteps(WithPaging):
    """The response for a Steps query containing matched steps."""

    steps: List[Step]
    """A list of all the steps in this page."""

    total_count: Optional[int] = None
    """The total number of steps that match the query."""
