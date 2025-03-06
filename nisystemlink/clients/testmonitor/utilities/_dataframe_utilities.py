from typing import Any, Dict, List

import pandas as pd
from nisystemlink.clients.testmonitor.models import (
    Step,
    StepProjection,
)
from pandas import DataFrame


def convert_steps_to_dataframe(steps: List[Step]) -> DataFrame:
    """Converts a list of steps into a normalized dataframe

    Args:
        steps (List[Step]): A list of steps.

    Returns:
        DataFrame: A Pandas DataFrame containing the normalized steps data.
    """
    steps_dict_representation = [step.dict(exclude_unset=True) for step in steps]
    restructured_steps = __restructure_steps(steps=steps_dict_representation)

    normalized_steps_dataframe = pd.json_normalize(restructured_steps, sep=".")
    grouped_columns = __group_step_columns(normalized_steps_dataframe.columns)
    normalized_steps_dataframe = normalized_steps_dataframe.reindex(
        columns=grouped_columns
    )
    normalized_steps_dataframe.dropna(axis="columns", how="all", inplace=True)

    return normalized_steps_dataframe


def __restructure_steps(steps: List[Dict[str, Any]]) -> List:
    """Restructures the list of inputs and outputs into dictionaries, with the key as the input or
    output's name and value as the actual value of the input or output respectively.

    This will be helpful when normalizing the steps into a dataframe. If not, then the inputs and outputs
    will be defined as an array of values, within a single cell in the dataframe respectively.

    Args:
        steps (List): A list of step responses retrieved from the API.

    Returns:
        List[Step]: Restructured steps - modification involves the conversion of list of inputs and outputs
        into dictionaries respectively.
    """

    def process_io(io_list: List) -> Dict:
        return {io["name"]: io["value"] for io in io_list}

    input_key = StepProjection.INPUTS.lower()
    output_key = StepProjection.OUTPUTS.lower()

    for step in steps:
        if input_key in step and step[input_key]:
            step[input_key] = process_io(step.get(input_key, []))
        if output_key in step and step[output_key]:
            step[output_key] = process_io(step.get(output_key, []))

    return steps


def __group_step_columns(df_columns: List[str]) -> List[str]:
    """Gets the list of columns in the dataframe, group them under various categories and orders them.

    When normalizing the steps into a dataframe, there would be inconsistency in the ordering of the
    columns. For example, consider from a list of steps the first step has been added as a column.
    Now when including the next step, if there are new input, output or property fields, they would get
    added as the last column in the dataframe, which would break the actual expected column flow in the
    dataframe. Using this function, the columns can be grouped together.

    Args:
        df_columns (List[str]): The list of all columns from the normalized dataframe.

    Returns:
        List[str]: A list containing grouped and ordered columns.
    """
    grouped_columns: Dict[str, List[str]] = {
        "general": [],
        StepProjection.INPUTS: [],
        StepProjection.OUTPUTS: [],
        StepProjection.DATA: [],
        StepProjection.PROPERTIES: [],
    }

    for column in df_columns:
        if StepProjection.DATA.lower() in column and not column == "data_model":
            grouped_columns[StepProjection.DATA].append(column)
        elif StepProjection.INPUTS.lower() in column:
            grouped_columns[StepProjection.INPUTS].append(column)
        elif StepProjection.OUTPUTS.lower() in column:
            grouped_columns[StepProjection.OUTPUTS].append(column)
        elif StepProjection.PROPERTIES.lower() in column:
            grouped_columns[StepProjection.PROPERTIES].append(column)
        else:
            grouped_columns["general"].append(column)

    return (
        grouped_columns["general"]
        + grouped_columns[StepProjection.INPUTS]
        + grouped_columns[StepProjection.OUTPUTS]
        + grouped_columns[StepProjection.DATA]
        + grouped_columns[StepProjection.PROPERTIES]
    )
