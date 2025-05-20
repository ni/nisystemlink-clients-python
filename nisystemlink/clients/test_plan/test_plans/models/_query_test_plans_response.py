from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from ._test_plan import TestPlan


class QueryTestPlansResponse(JsonModel):
    """
    Represents the response from querying test plans.
    Contains a list of test plans, a continuation token for pagination, and the total count.
    """

    test_plans: Optional[List[TestPlan]]
    """A list of test plans returned by the query."""

    continuation_token: Optional[str] = None
    """A token to retrieve the next page of results for paginated queries."""

    total_count: Optional[int] = None
    """The total number of test plans matching the query filter."""
