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

    # checking if `data` exists in the steps. the following logic is specific to process `data` field
    if steps and steps[0].data:
        steps_dataframe = pd.json_normalize(restructured_steps, sep=".").explode(
            DATA_PARAMETERS, ignore_index=True
        )
        steps_dataframe = pd.concat(
            [
                steps_dataframe.drop(columns=[DATA_PARAMETERS]),
                pd.json_normalize(steps_dataframe[DATA_PARAMETERS]).add_prefix(
                    f"{DATA_PARAMETERS}."
                ),
            ],
            axis=1,
        )
    else:
        steps_dataframe = pd.json_normalize(restructured_steps, sep=".")

    grouped_columns = __group_step_columns(steps_dataframe.columns)

    return steps_dataframe.reindex(columns=grouped_columns)


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
    restructured_steps = []

    for step in steps:
        step_dict = step.dict(exclude_none=True)
        step_dict[StepProjection.INPUTS.lower()] = (
            {item.name: item.value for item in step.inputs} if step.inputs else {}
        )
        step_dict[StepProjection.OUTPUTS.lower()] = (
            {item.name: item.value for item in step.outputs} if step.outputs else {}
        )

        restructured_steps.append(step_dict)

    return restructured_steps


def __group_step_columns(df_columns: List[str]) -> List[str]:
    """Groups and orders dataframe columns into predefined categories to maintain a consistent structure.

    When normalizing steps into a dataframe, new input, output, or property fields may be added at the end,
    disrupting the expected column order. This function ensures columns are grouped properly.

    Args:
        df_columns: The list of all columns from the normalized dataframe.

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

    for column in df_columns:
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
