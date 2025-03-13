from typing import Any, Dict, List

import pandas as pd
from nisystemlink.clients.testmonitor.models import Result
from nisystemlink.clients.testmonitor.utilities.constants import DataFrameHeaders


def convert_results_to_dataframe(
    results: List[Result], set_id_as_index: bool = True
) -> pd.DataFrame:
    """Creates a Pandas DataFrame for the results.

    Args:
        results: The list of results to be included in the dataframe.
        set_id_as_index: If true (default value), result id will be set as index for the dataframe.
                         If false, index will not be set.

    Returns:
        A Pandas DataFrame with the each result fields having a separate column.
        Following fields are split into sub-columns.
            - status_type_summary: All the entries will be split into separate columns.
            For example, status_type_summary.LOOPING, status_type_summary.PASSED, etc
            - status: Split into status.status_type and status.status_name columns.
            - Properties: All the properties will be split into separate columns. For example,
            properties.property1, properties.property2, etc.
    """
    results_dict = [result.dict(exclude_none=True) for result in results]
    results_dict_with_normalized_status = __normalize_results_status(results_dict)
    normalized_dataframe = pd.json_normalize(
        results_dict_with_normalized_status, sep="."
    )
    normalized_dataframe = __format_results_columns(
        results_dataframe=normalized_dataframe
    )
    if set_id_as_index and "id" in normalized_dataframe.columns:
        normalized_dataframe.set_index("id", inplace=True)

    return normalized_dataframe


def __normalize_results_status(
    results_dict: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Gets dictionary of results data and modifies the status object.

    Args:
        results: List of results.

    Returns:
        A list of result fields as dictionary. If status.status_type is "CUSTOM"
            the status field takes the value of "status_name", else value of "status_type" is used.
    """
    for result in results_dict:
        status = result.get("status", {})
        if status.get("status_type") == "CUSTOM":
            result["status"] = status["status_name"]
        else:
            result["status"] = status["status_type"].value

    return results_dict


def __format_results_columns(results_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Format results column to keep properties at the end.

    Args:
        results_dataframe: Dataframe of results.

    Returns:
        Formatted dataframe of results.
    """
    column_headers = results_dataframe.columns.to_list()
    standard_column_headers = [
        header for header in column_headers if __is_standard_column_header(header)
    ]
    status_type_summary_header = [
        header
        for header in column_headers
        if __is_status_type_summary_header(header=header)
    ]
    properties_headers = [
        header for header in column_headers if __is_property_header(header=header)
    ]
    standard_column_headers += status_type_summary_header + properties_headers

    return results_dataframe.reindex(columns=standard_column_headers, copy=False)


def __is_standard_column_header(header: str) -> bool:
    """Check if column header is not status type summary or property.

    Args:
        header: column header for results dataframe.

    Returns:
        True if header doesn't start with 'status_type_summary.', 'properties.'. Else returns false.

    """
    return not (
        __is_status_type_summary_header(header=header)
        or __is_property_header(header=header)
    )


def __is_status_type_summary_header(header: str) -> bool:
    """Check if column header is not a status type summary.

    Args:
        header: column header for results dataframe.

    Returns:
        True if header contains 'status_type_summary.'. Else returns false.

    """
    return header.startswith(DataFrameHeaders.STATUS_TYPE_SUMMARY_HEADER_PREFIX)


def __is_property_header(header: str) -> bool:
    """Check if column header is not a property.

    Args:
        header: column header for results dataframe.

    Returns:
        True if header contains 'properties.'. Else returns false.

    """
    return header.startswith(DataFrameHeaders.PROPERTY_COLUMN_HEADER_PREFIX)
