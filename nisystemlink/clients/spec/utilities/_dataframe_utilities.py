from typing import Callable, Dict, List, Optional, Union

import pandas as pd
from nisystemlink.clients.spec.models._condition import (
    Condition,
    NumericConditionValue,
    StringConditionValue,
)
from nisystemlink.clients.spec.models._specification import Specification
from nisystemlink.clients.spec.utilities._constants import DataFrameHeaders


def __serialize_conditions(conditions: List[Condition]) -> Dict[str, str]:
    """Serialize conditions into desired format.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a dictionary.
    """
    return {
        __generate_condition_column_header(condition): ", ".join(
            __get_condition_values(condition)
        )
        for condition in conditions
        if condition.name and condition.value
    }


def convert_specs_to_dataframe(
    specs: List[Specification],
    condition_format: Optional[
        Callable[[List[Condition]], Dict]
    ] = __serialize_conditions,
) -> pd.DataFrame:
    """Format specs with respect to the provided condition format.

    Args:
        specs: List of specs of the specified products.
        condition_format: Function which takes in a list of condition objects and returns
                          a dictionary of condition and its values. The dictionary keys
                          should be the condition name and the values should be the condition
                          value in any format you need. Keys will be used as the dataframe
                          column header and values will be used as the row cells for the
                          respective column header. If not passed, default condition format will be used.
                          By default, for all the condition columns to be grouped
                          together in the dataframe, the dictionary key should have the prefix "condition_".
                          This is an optional parameter. By default column header will be
                          "condition_<conditionName>(<conditionUnit>)".
                          The column value will be "[min: num; max: num, step: num], num, num"
                          where data within the '[]' is numeric condition range and other num
                          values are numeric condition discrete values.
                          The column value will be "str, str, str" - where str values are the
                          condition discrete values for a string condition. If the condition doesn't
                          have values, it will not be added to the dataframe.

    Returns:
        The list of specs of the specified product as a dataframe. Condition column will be formatted based on the
        condition_format method. If condition_format is not passed while calling, default condition
        formatting will be done. By default, if condition value is numeric condition value column names
        will be in "condition_conditionName(conditionUnit)" format and column values will be in
        "[min: num; max: num, step: num], num, num" format where data within the '[]' is numeric
        condition range and other num values are numeric condition discrete values. And if condition
        value is string condition value, the column header will be in "condition_conditionName" format
        and column values will be in "str, str, str" format where str values are the condition discrete
        values for a string condition.
    """
    specs_dict = [
        {
            **{key: value for key, value in vars(spec).items() if key != "conditions"},
            **(
                condition_format(spec.conditions)
                if condition_format and spec.conditions
                else {}
            ),
        }
        for spec in specs
    ]

    specs_dataframe = pd.json_normalize(specs_dict)
    specs_dataframe = __format_specs_columns(specs_dataframe=specs_dataframe)
    specs_dataframe.dropna(axis="columns", how="all", inplace=True)

    return specs_dataframe


def __format_specs_columns(specs_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Format specs column to group conditions and keep properties and keywords at the end.

    Args:
        specs_dataframe: Dataframe of specs.

    Returns:
        Formatted dataframe of specs.
    """
    column_headers = specs_dataframe.columns.to_list()
    formatted_column_headers = [
        header for header in column_headers if __is_standard_column_header(header)
    ]
    condition_headers = [
        header for header in column_headers if __is_condition_header(header=header)
    ]
    properties_headers = [
        header for header in column_headers if __is_property_header(header=header)
    ]
    formatted_column_headers += (
        condition_headers
        + (["keywords"] if "keywords" in column_headers else [])
        + properties_headers
    )

    return specs_dataframe.reindex(columns=formatted_column_headers)


def __is_standard_column_header(header: str) -> bool:
    """Check if column header is not a condition, property or keywords.

    Args:
        header: column header for specs dataframe.

    Returns:
        True if header doesn't start with condition_, properties. or keywords. Else returns false.

    """
    return not (
        __is_condition_header(header=header)
        or __is_property_header(header=header)
        or __is_keywords_header(header=header)
    )


def __is_condition_header(header: str) -> bool:
    """Check if column header is not a condition.

    Args:
        header: column header for specs dataframe.

    Returns:
        True if header contains 'condition_'. Else returns false.

    """
    return header.startswith(DataFrameHeaders.CONDITION_COLUMN_HEADER_PREFIX)


def __is_property_header(header: str) -> bool:
    """Check if column header is not a property.

    Args:
        header: column header for specs dataframe.

    Returns:
        True if header contains 'properties.'. Else returns false.

    """
    return header.startswith(DataFrameHeaders.PROPERTY_COLUMN_HEADER_PREFIX)


def __is_keywords_header(header: str) -> bool:
    """Check if column header is not a keywords.

    Args:
        header: column header for specs dataframe.

    Returns:
        True if header equals 'keywords'. Else returns false.

    """
    return header == DataFrameHeaders.KEYWORDS_COLUMN_HEADER


def __generate_condition_column_header(condition: Condition) -> str:
    """Generate column header for a condition.

    Args:
        condition: Condition object for generating column header.

    Returns:
        The column header for the given condition.
    """
    name = condition.name or ""
    unit = (
        f"({condition.value.unit})"
        if isinstance(condition.value, NumericConditionValue) and condition.value.unit
        else ""
    )

    return f"condition_{name}{unit}"


def __get_condition_values(condition: Condition) -> List[str]:
    """Get ranges and discrete values of a condition.

    Args:
        condition: Condition for getting values.

    Returns:
        The list of values of the given condition in a specific format.
    """
    if not condition.value:
        return []

    values = []

    if isinstance(condition.value, NumericConditionValue):
        values.extend(__serialize_numeric_condition_range(value=condition.value))

    values.extend(__serialize_condition_discrete_values(value=condition.value))

    return values


def __serialize_numeric_condition_range(value: NumericConditionValue) -> List[str]:
    """Serialize ranges of a numeric condition value.

    Args:
        value: A condition's value with NumericConditionValue type.

    Returns:
        The list of ranges of the given value in a specific format.
    """
    if not value.range:
        return []

    return [
        f"[{'; '.join(
            f'{range_key}: {range_value}'
            for range_key, range_value in vars(range).items()
            if range_value is not None
        )}]"
        for range in value.range
    ]


def __serialize_condition_discrete_values(
    value: Union[NumericConditionValue, StringConditionValue]
) -> List[str]:
    """Serialize discrete values of a value.

    Args:
        value: A condition's value with either NumericConditionValue type or StringConditionValue type.

    Returns:
        The list of discrete values of the given value in a string format.
    """
    return [str(discrete) for discrete in (value.discrete or [])]
