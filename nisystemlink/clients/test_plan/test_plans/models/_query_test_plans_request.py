from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class QueryTestPlansRequest(JsonModel):
    """
    Represents the request body for querying test plans.
    Allows filtering, sorting, and pagination of test plan results.
    """

    filter: Optional[str] = None
    """A string expression to filter the test plans returned by the query."""

    take: Optional[int] = None
    """The maximum number of test plans to return in the response."""

    order_by: Optional[str] = None
    """The field name to use for sorting the test plans."""

    descending: Optional[bool] = None
    """Whether to sort the test plans in descending order."""

    return_count: Optional[bool] = None
    """Whether to include the total count of matching test plans in the response."""

    continuation_token: Optional[str] = None
    """A token to retrieve the next page of results for paginated queries."""
