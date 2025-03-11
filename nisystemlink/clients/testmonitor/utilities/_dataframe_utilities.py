from typing import Any, Dict, List

import pandas as pd
from nisystemlink.clients.testmonitor.models import (
    Step,
    StepProjection,
)
from pandas import DataFrame


def convert_steps_to_dataframe(steps: List[Step]) -> DataFrame:
    """Converts a list of steps into a normalized dataframe.

    Args:
        steps: A list of steps.

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

    step_dicts = __convert_steps_to_dict(steps)

    steps_dataframe = pd.json_normalize(step_dicts, sep=".")
    steps_dataframe = __explode_and_normalize(
        steps_dataframe, DATA_PARAMETERS, f"{DATA_PARAMETERS}."
    )

    grouped_columns = __group_step_columns(steps_dataframe.columns)

    return steps_dataframe.reindex(columns=grouped_columns, copy=False)


def __convert_steps_to_dict(steps: List[Step]) -> List[Dict[str, Any]]:
    """Converts a list of steps to dictionaries, excluding None values.

    Args:
        steps: A list of steps.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing step information.
    """
    steps_dict = []

    for step in steps:
        single_step_dict = step.dict(exclude_none=True)
        __normalize_inputs_outputs(single_step_dict, step)
        steps_dict.append(single_step_dict)

    return steps_dict


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
                if column_lower.startswith(f"{category.lower()}.")
                and column != StepProjection.DATA_MODEL.lower()
            ),
            GENERAL_CATEGORIES,
        )
        grouped_columns[key].append(column)

    return [
        column for category in CATEGORY_KEYS for column in grouped_columns[category]
    ]
