from typing import List

import pandas as pd
from nisystemlink.clients.testmonitor.models import Result


def convert_results_to_dataframe(results: List[Result]) -> pd.DataFrame:
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
