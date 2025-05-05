from typing import Any, Callable, Dict, List, Optional

import pandas as pd
from nisystemlink.clients.testmonitor.models import (
    Measurement,
    Result,
    Step,
    StepProjection,
)
from nisystemlink.clients.testmonitor.utilities.constants import DataFrameHeaders


def has_name_and_measurement(measurement: Measurement) -> bool:
    """Checks if a step data parameter is measurement data by ensuring it has both
    'name' and 'measurement' fields.

    Args:
        measurement: A measurement data object

    Returns:
        bool: True if the measurement has both 'name' and 'measurement' fields, False otherwise.
    """
    return measurement.name is not None and measurement.measurement is not None


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
            - Properties: All the properties will be split into separate columns. For example,
            properties.property1, properties.property2, etc.
    """
    results_dict = []
    for result in results:
        data = result.model_dump(exclude_none=True)
        __normalize_status(data)
        results_dict.append(data)

    normalized_dataframe = pd.json_normalize(results_dict, sep=".")
    normalized_dataframe = __format_results_columns(
        results_dataframe=normalized_dataframe
    )
    if set_id_as_index and "id" in normalized_dataframe.columns:
        normalized_dataframe.set_index("id", inplace=True)

    return normalized_dataframe


def convert_steps_to_dataframe(
    steps: List[Step],
    is_valid_measurement: Optional[
        Callable[[Measurement], bool]
    ] = has_name_and_measurement,
) -> pd.DataFrame:
    """Converts a list of steps into a normalized dataframe.

    Args:
        steps: A list of steps.
        is_valid_measurement: Optional callback function that checks if a step data parameter is a
            valid measurement so that only those are included in the returned dataframe. The method takes
            a measurement as input and returns a boolean value.
            The default behavior is to consider only measurement data that have both 'name' and 'measurement'
            fields with values as valid measurements.
            If none of the measurements have the required fields, the step data parameters will not
            appear in the dataframe.
            If the callback function is set to None, all step data parameters will be included in the dataframe.

    Returns:
        DataFrame:
            - A Pandas DataFrame containing the steps data. The DataFrame would consist of all the
            fields in the input steps.
            - A new column would be created for unique `properties` across all steps. The property
            columns would be named in the format `properties.property_name`.
            - A new column would be created for unique `Inputs` and `Outputs` across all steps. The columns
            would be named in the format `inputs.input_name` and `outputs.output_name` respectively.
            - The column headers for the step data parameters would differ based on the callback function. If
            the None is passed for the callback function, the column would be prefixed with `data.parameters.`.
            If the callback function is set, the column would be prefixed with `data.measurement.`.
    """
    DATA_PARAMETERS_PREFIX = (
        "data.parameters" if is_valid_measurement is None else "data.measurement"
    )
    step_dicts = __convert_steps_to_dict(steps, is_valid_measurement)
    steps_dataframe = pd.json_normalize(step_dicts, sep=".")
    steps_dataframe = __explode_and_normalize(
        steps_dataframe, "data.parameters", f"{DATA_PARAMETERS_PREFIX}."
    )
    grouped_columns = __group_step_columns(steps_dataframe.columns)
    return steps_dataframe.reindex(columns=grouped_columns, copy=False)


def __normalize_status(
    data: Dict[str, Any],
) -> None:
    """Normalizes the status object into a string.

    Args:
        data: Dictionary containing status information.

    """
    status = data.get("status", {})
    if status:
        if status.get("status_type") == "CUSTOM":
            data["status"] = status.get("status_name", None)
        else:
            data["status"] = getattr(status.get("status_type", None), "value", None)


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
    is_valid_measurement: Optional[Callable[[Measurement], bool]],
) -> List[Dict[str, Any]]:
    """Converts a list of steps to dictionaries, excluding None values.

    Args:
        steps: A list of steps.
        is_valid_measurement: Optional callback function that checks if a step data
            parameter is a valid measurement so that only those are included in the returned dataframe.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing step information.
    """
    steps_dict = []
    for step in steps:

        single_step_dict = step.model_dump(exclude_none=True)
        __filter_invalid_measurements(single_step_dict, step, is_valid_measurement)
        __normalize_inputs_outputs(single_step_dict, step)
        __normalize_status(single_step_dict)
        steps_dict.append(single_step_dict)
    return steps_dict


def __filter_invalid_measurements(
    step_dict: Dict[str, Any],
    step: Step,
    is_valid_measurement: Optional[Callable[[Measurement], bool]],
) -> None:
    """Gets data parameters from the step dictionary and filters it based on the callback function.

    Args:
        step_dict: A dictionary with step information.
        step: A Step object containing data parameters.
        is_valid_measurement: Optional callback function to check if a measurement is valid. The method takes
            a Measurement as input and returns a boolean value. The default behavior is to consider only parameters
            that have both 'name' and 'measurement' fields with values as valid measurements.

    Returns:
        None: The function modifies step dictionary in place with filtered data parameters.
    """
    if step.data and step.data.parameters and is_valid_measurement is not None:
        valid_measurement_parameters = []
        for measurement in step.data.parameters:
            if measurement and is_valid_measurement(measurement):
                valid_measurement_parameters.append(measurement)

        step_dict["data"]["parameters"] = [
            measurement.model_dump(exclude_none=True)
            for measurement in valid_measurement_parameters
        ]


def __normalize_inputs_outputs(
    step_dict: Dict[str, Any],
    step: Step,
) -> None:
    """Normalizes the input and output fields by converting them into dictionaries.

    Args:
        step_dict: A dictionary with step information.
        step: A Step object containing inputs and outputs.

    Returns:
        None: The function modifies step_dict in place with normalized inputs and outputs.
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
        return pd.concat([exploded_dataframe, normalized_dataframe], axis=1, copy=False)
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
    CATEGORY_KEYS = DataFrameHeaders.CATEGORY_COLUMN_HEADERS
    grouped_columns: Dict[str, List[str]] = {category: [] for category in CATEGORY_KEYS}
    for column in dataframe_columns:
        column_lower = column.lower()
        key = next(
            (
                category
                for category in CATEGORY_KEYS[1:]
                if column_lower.startswith(category)
                and column != StepProjection.DATA_MODEL.lower()
            ),
            GENERAL_CATEGORIES,
        )
        grouped_columns[key].append(column)
    return [
        column
        for category_key in CATEGORY_KEYS
        for column in grouped_columns[category_key]
    ]
