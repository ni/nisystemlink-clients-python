from typing import Any, Dict, List

import pandas as pd
from nisystemlink.clients.testmonitor.models import (
    Step,
    StepProjection,
)
from pandas import DataFrame


def convert_steps_to_dataframe(steps: List[Step]) -> DataFrame:
    """Converts a list of steps into a normalized dataframe.

    - A new column would be created for unique `properties` across all steps. The property
    columns would be named in the format `properties.property_name`.
    - `Inputs` and `Outputs` are converted from a list of name-value pairs to a dict and then
    normalized - similar to properties.
    - For each `parameter` entry in `data`, a new row is added in the dataframe, with all the
    other values are duplicated.

    Args:
        steps: A list of steps.

    Returns:
        DataFrame:
            - A Pandas DataFrame containing the steps data. The DataFrame would consist of all the
            fields in the input steps.
            - A new column would be created for unique `properties` across all steps. The property
            columns would be named in the format `properties.property_name`.
            - `Inputs` and `Outputs` are converted from a list of name-value pairs to a dict and then
            normalized - similar to properties.
            - For each `parameter` entry in `data`, a new row is added in the dataframe, with all the
            other values are duplicated.
    """
    DATA_PARAMETERS = "data.parameters"

    restructured_steps = __restructure_steps(steps)

    steps_dataframe = pd.json_normalize(restructured_steps, sep=".")
    if DATA_PARAMETERS in steps_dataframe.columns.to_list():
        steps_dataframe = __explode_and_normalize(
            steps_dataframe, DATA_PARAMETERS, f"{DATA_PARAMETERS}."
        )

    grouped_columns = __group_step_columns(steps_dataframe.columns)

    return steps_dataframe.reindex(columns=grouped_columns)


def __explode_and_normalize(
    dataframe: DataFrame, column: str, prefix: str
) -> DataFrame:
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


def __restructure_steps(steps: List[Step]) -> List[Dict[str, Any]]:
    """Restructures a list of step responses by converting input and output lists into dictionaries.

    Each dictionary maps input/output names to their corresponding values, making it easier to
    normalize the data into a DataFrame. Without this transformation, inputs and outputs would
    remain as lists within a single cell.

    Args:
        steps: A list of step responses retrieved from the API.

    Returns:
        List[Step]: Restructured steps - modification involves the conversion of list of inputs and outputs
        into dictionaries respectively.
    """
    INPUTS = StepProjection.INPUTS.lower()
    OUTPUTS = StepProjection.OUTPUTS.lower()
    restructured_steps = []

    for step in steps:
        step_dict = step.dict(exclude_none=True)
        if INPUTS in step_dict:
            step_dict[INPUTS] = (
                {item.name: item.value for item in step.inputs} if step.inputs else {}
            )
        if OUTPUTS in step_dict:
            step_dict[OUTPUTS] = (
                {item.name: item.value for item in step.outputs} if step.outputs else {}
            )

        restructured_steps.append(step_dict)

    return restructured_steps


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
        if (
            StepProjection.DATA.lower() in column_lower
            and column != StepProjection.DATA_MODEL.lower()
        ):
            grouped_columns[StepProjection.DATA].append(column)
        elif StepProjection.INPUTS.lower() in column_lower:
            grouped_columns[StepProjection.INPUTS].append(column)
        elif StepProjection.OUTPUTS.lower() in column_lower:
            grouped_columns[StepProjection.OUTPUTS].append(column)
        elif StepProjection.PROPERTIES.lower() in column_lower:
            grouped_columns[StepProjection.PROPERTIES].append(column)
        else:
            grouped_columns[GENERAL_CATEGORIES].append(column)

    return [
        column for category in CATEGORY_KEYS for column in grouped_columns[category]
    ]
