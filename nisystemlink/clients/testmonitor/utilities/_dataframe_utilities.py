from typing import Any, Callable, Dict, List, Optional

import pandas as pd
from nisystemlink.clients.testmonitor.models import Result, Step, StepProjection
from nisystemlink.clients.testmonitor.utilities.constants import DataFrameHeaders


def convert_results_to_dataframe(
    results: List[Result], set_id_as_index: bool = True
) -> pd.DataFrame:
    """Creates a Pandas DataFrame for the results.

    Args:
        results: The list of results to be included in the dataframe.
        set_id_as_index: If true, result id will be set as index for the dataframe.
                         If false, index will not be set.
                         Default value is false.

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


def convert_steps_to_dataframe(
    steps: List[Step],
    is_valid_measurement: Optional[Callable[[Dict[str, Any]], bool]] = None,
) -> pd.DataFrame:
    """Converts a list of steps into a normalized dataframe.

    Args:
        steps: A list of steps.
        is_valid_measurement: Optional function to check if a measurement is valid. The method takes
            a dictionary as input and returns a boolean value. If the function is not provided, the
            default behavior is to keep only those measurements that have both 'name' and 'measurement' fields.
            If none of the measurement data have the desired fields, the data.parameters will not
            appear in the dataframe.

    Returns:
        DataFrame:
            - A Pandas DataFrame containing the steps data. The DataFrame would consist of all the
            fields in the input steps.
            - A new column would be created for unique `properties` across all steps. The property
            columns would be named in the format `properties.property_name`.
            - A new column would be created for unique `Inputs` and `Outputs` across all steps. The columns
            would be named in the format `inputs.input_name` and `outputs.output_name` respectively.
            - For each `parameter` entry in `data`, a new row is added in the dataframe, with data for
            all other step fields are duplicated.
    """
    DATA_PARAMETERS = "data.parameters"
    step_dicts = __convert_steps_to_dict(steps, is_valid_measurement)
    steps_dataframe = pd.json_normalize(step_dicts, sep=".")
    steps_dataframe = __explode_and_normalize(
        steps_dataframe, DATA_PARAMETERS, f"{DATA_PARAMETERS}."
    )
    grouped_columns = __group_step_columns(steps_dataframe.columns)
    return steps_dataframe.reindex(columns=grouped_columns, copy=False)


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


def __convert_steps_to_dict(
    steps: List[Step],
    is_valid_measurement: Optional[Callable[[Dict[str, Any]], bool]] = None,
) -> List[Dict[str, Any]]:
    """Converts a list of steps to dictionaries, excluding None values.

    Args:
        steps: A list of steps.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing step information.
    """
    steps_dict = []
    for step in steps:
        single_step_dict = step.dict(exclude_none=True)

        if step.data is not None and step.data.parameters is not None:
            single_step_dict["data"]["parameters"] = __get_valid_data_parameters(
                single_step_dict, is_valid_measurement
            )

        __normalize_inputs_outputs(single_step_dict, step)
        __normalize_step_status(single_step_dict)
        steps_dict.append(single_step_dict)
    return steps_dict


def __get_valid_data_parameters(
    step_dict: Dict[str, Any],
    is_valid_measurement: Optional[Callable[[Dict[str, Any]], bool]] = None,
) -> List[Dict[str, Any]]:
    """Gets valid measurement data parameters from the step dictionary.

    Args:
        step_dict: A dictionary with step information.
        is_valid_measurement: Optional callback function to check if a measurement is valid. The method takes
            a dictionary as input and returns a boolean value. If the function is not provided, the
            default behavior is to keep only those measurements that have both 'name' and 'measurement' fields.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing valid measurement data.
    """
    allowed_measurement_keys = ["name", "units"]
    valid_measurement_parameters = []
    for parameter in step_dict["data"]["parameters"]:
        if (is_valid_measurement and is_valid_measurement(parameter)) or all(
            key in parameter for key in allowed_measurement_keys
        ):
            valid_measurement_parameters.append(parameter)

    return valid_measurement_parameters


def __normalize_inputs_outputs(
    step_dict: Dict[str, Any],
    step: Step,
) -> None:
    """Normalizes the input and output fields by converting them into dictionaries.

    Args:
        step_dict: A dictionary with step information.
        step: A Step object containing inputs and outputs.

    Returns:
        None: The function modifies step_dict in place.
    """
    STEP_INPUTS = StepProjection.INPUTS.lower()
    STEP_OUTPUTS = StepProjection.OUTPUTS.lower()
    if STEP_INPUTS in step_dict:
        step_dict[STEP_INPUTS] = (
            {item.name: item.value for item in step.inputs} if step.inputs else {}
        )
    if STEP_OUTPUTS in step_dict:
        step_dict[STEP_OUTPUTS] = (
            {item.name: item.value for item in step.outputs} if step.outputs else {}
        )


def __normalize_step_status(step_dict: Dict[str, Any]) -> None:
    step_status = step_dict.get("status", {})
    if step_status.get("status_type") == "CUSTOM":
        step_dict["status"] = step_status.get("status_name", None)
    else:
        step_dict["status"] = step_status["status_type"].value


def __explode_and_normalize(
    dataframe: pd.DataFrame, column: str, prefix: str
) -> pd.DataFrame:
    """Explodes a specified column in the dataframe and normalizes its nested data.
    This function handles the process of exploding a column that contains lists or arrays,
    transforming each list element into a separate row. After exploding, it normalizes the
    nested data into flat columns using the specified prefix, making it easier to analyze
    and manipulate. The new columns are added to the original dataframe.

    Args:
        dataframe: The input DataFrame that contains the column to explode and normalize.
        column: The name of the column in the DataFrame that contains the list-like data to explode.
        prefix: The prefix to add to the new column names created during the normalization process.

    Returns:
        DataFrame:
        - A new DataFrame with the exploded rows and the normalized columns, all combined
        with the original data in the dataframe.
        - If the column is not found in the dataframe, the original dataframe is returned unchanged.
    """
    if column in dataframe:
        exploded_dataframe = dataframe.explode(column, ignore_index=True)
        normalized_dataframe = pd.json_normalize(
            exploded_dataframe.pop(column)
        ).add_prefix(prefix)
        return pd.concat([exploded_dataframe, normalized_dataframe], axis=1)
    return dataframe


def __group_step_columns(dataframe_columns: List[str]) -> List[str]:
    """Groups and orders dataframe columns into predefined categories to maintain a consistent structure.
    When normalizing steps into a dataframe, new input, output, or property fields may be added at the end,
    disrupting the expected column order. This function ensures columns are grouped properly.

    Args:
        dataframe_columns: The list of all columns from the normalized dataframe.

    Returns:
        List[str]: A list containing grouped and ordered columns.
    """
    GENERAL_CATEGORIES = "general"
    CATEGORY_KEYS = [
        GENERAL_CATEGORIES,
        StepProjection.INPUTS,
        StepProjection.OUTPUTS,
        StepProjection.DATA,
        StepProjection.PROPERTIES,
    ]
    grouped_columns: Dict[str, List[str]] = {category: [] for category in CATEGORY_KEYS}
    for column in dataframe_columns:
        column_lower = column.lower()
        key = next(
            (
                category
                for category in CATEGORY_KEYS
                if column_lower.startswith(category.lower())
                and column != StepProjection.DATA_MODEL.lower()
            ),
            GENERAL_CATEGORIES,
        )
        grouped_columns[key].append(column)
    return [
        column for category in CATEGORY_KEYS for column in grouped_columns[category]
    ]
