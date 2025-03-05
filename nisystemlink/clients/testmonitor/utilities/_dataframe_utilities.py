from typing import List, Optional

import pandas as pd
from nisystemlink.clients.testmonitor._test_monitor_client import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    Result,
    ResultProjection,
)
from nisystemlink.clients.testmonitor.utilities._client_utilities import (
    __batch_query_results,
)


def get_results_dataframe(
    client: TestMonitorClient,
    query_filter: str,
    column_projection: Optional[List[ResultProjection]] = None,
) -> pd.DataFrame:
    """Fetches test results and normalizes them into a Pandas DataFrame.

    Args:
        client: The TestMonitorClient to use for the request.
        query_filter: The result query filter in Dynamic Linq format.
        column_projection: List of columns to retrieve when querying the results.
            Fields you do not specify are excluded. Returns all fields if no value is specified.

    Returns:
        A Pandas DataFrame containing the results.

    Raises:
        ApiException: If unable to communicate with the `/nitestmonitor` service
            or provided an invalid argument.
    """
    queried_results = __batch_query_results(client, query_filter, column_projection)

    results_dataframe = __normalize_results(queried_results)

    return results_dataframe


def __normalize_results(results: List[Result]) -> pd.DataFrame:
    """Normalizes the results into a Pandas DataFrame.

    Args:
        results: The list of results to normalize.

    Returns:
        A Pandas DataFrame with the normalized queried results.
    """
    results_dict = [result.dict(exclude_unset=True) for result in results]
    normalized_dataframe = pd.json_normalize(results_dict, sep=".")
    normalized_dataframe.dropna(axis="columns", how="all", inplace=True)

    return normalized_dataframe
