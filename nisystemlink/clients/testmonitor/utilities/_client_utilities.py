from typing import List, Optional

from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    QueryResultsRequest,
    Result,
    ResultProjection,
)
from nisystemlink.clients.testmonitor.utilities._constants import HttpConstants


def __batch_query_results(
    client: TestMonitorClient,
    query_filter: str,
    column_projection: Optional[List[ResultProjection]] = None,
) -> List[Result]:
    """Fetches test results in batches.

    Args:
        client: The TestMonitorClient to use for the request.
        query_filter: The result query filter in Dynamic Linq format.
        column_projection: List of columns to retrieve when querying the results.
            Fields you do not specify are excluded. Returns all fields if no value is specified.

    Returns:
        A list of results.
    """
    all_results: List[Result] = []
    query_request = QueryResultsRequest(
        filter=query_filter,
        projection=column_projection,
        take=HttpConstants.DEFAULT_QUERY_RESULTS_TAKE,
    )

    query_response = client.query_results(query_request)
    all_results.extend(query_response.results)

    while query_response.continuation_token:
        query_request.continuation_token = query_response.continuation_token
        query_response = client.query_results(query_request)
        all_results.extend(query_response.results)

    return all_results
