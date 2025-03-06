from typing import List

import pandas as pd
from nisystemlink.clients.testmonitor.models import Result


def convert_results_to_dataframe(results: List[Result]) -> pd.DataFrame:
    """Normalizes the results into a Pandas DataFrame.

    Args:
        results: The list of results to normalize.

    Returns:
        A Pandas DataFrame with the normalized queried results.
        status_type_summary will be normalized into the respective status types.
        For example, status_type_summary.LOOPING, status_type_summary.PASSED.
        Status is normalized into status.status_type and status.status_name.
        Properties are normalized into respective properties. For example,
        properties.property1, properties.property2 and etc.
    """
    results_dict = [result.dict(exclude_unset=True) for result in results]
    normalized_dataframe = pd.json_normalize(results_dict, sep=".")
    normalized_dataframe.dropna(axis="columns", how="all", inplace=True)

    return normalized_dataframe
