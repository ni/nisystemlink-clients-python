from typing import Any, Callable, Dict, List, Optional, Union

import pandas as pd
from nisystemlink.clients.spec.models._condition import (
    Condition,
    NumericConditionValue,
    StringConditionValue,
)
from nisystemlink.clients.spec.models._specification import (
    Specification,
    SpecificationLimit,
    SpecificationType,
)
from nisystemlink.clients.spec.utilities._constants import DataFrameHeaders


def summarize_conditions_as_a_string(
    conditions: List[Condition],
) -> List[Dict[str, str]]:
    """Converts the condition values to an easily readable string format that summarizes
    either of numeric or string condition.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a list of dictionary. The dictionary key will be
        "condition_<conditionName>(<conditionUnit>)".
        The dictionary value will be "[min: num; max: num, step: num], num, num"
        where data within the '[]' is numeric condition range and other num
        values are numeric condition discrete values.
        The dictionary value will be "str, str, str" - where str values are the
        condition discrete values for a string condition. If the condition doesn't
        have a name and value, it will be skipped.
    """
    return [
        {
            __generate_condition_column_header(condition): ", ".join(
                __serialize_condition_value(condition)
            )
            for condition in conditions
            if condition.name and condition.value
        }
    ]


def normalize_conditions_per_column(
    conditions: List[Condition],
) -> List[Dict[str, Any]]:
    """Convert conditions into list of dictionaries where dictionary key will be condition name
    and dictionary value will be condition value.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a list of dictionary. The key will be
        the condition name and the value will be the condition value which is
        either Numeric Condition Value, String Condition Value or None. If the condition doesn't
        have a name and value, it will be skipped.
    """
    return [
        {
            f"{DataFrameHeaders.CONDITION_COLUMN_HEADER_PREFIX}{condition.name}": condition.value
            for condition in conditions
            if condition.name and condition.value
        }
    ]


def normalize_conditions_per_row(
    conditions: List[Condition],
) -> List[Dict[str, Any]]:
    """Convert conditions into list of dictionaries where dictionary keys will be 'condition.name'
    and 'condition.value' and dictionary values will be condition name and condition value respectively.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a list of dictionary. The keys will be
        the 'condition.name' and 'condition.values' and the values will be the condition name and
        condition value which is either Numeric Condition Value, String Condition Value or None.
        If the condition doesn't have a name and value, it will be skipped.
        Each condition data will be logged as separate dictionary entry in the list which translates to
        separate row in the dataframe.
    """
    return [
        {"condition.name": condition.name, "condition.value": condition.value}
        for condition in conditions
        if condition.name and condition.value
    ]


def convert_specs_to_dataframe(
    specs: List[Specification],
    condition_format: Optional[
        Callable[[List[Condition]], List[Dict[str, Any]]]
    ] = normalize_conditions_per_column,
) -> pd.DataFrame:
    """Creates a Pandas DataFrame for the specs.

    Args:
        specs: List of specs.
        condition_format: A callback function which takes in a list of condition of a spec and returns
                          a list of dictionary of condition and its values. The dictionary keys
                          should be the condition name and the values should be the condition
                          value in any format you need. Dataframe rows will be constructed based on
                          these list of dictionaries. Each dictionary in the list indicates a row.
                          If there is more than one dictionary in the list, it will be considered as a new
                          row and other spec column data will be duplicated.  Keys will be used as the dataframe
                          column header and values will be used as the row cells for the
                          respective column header.
                          If not passed, condition column header will be condition name and
                          corresponding row value will be condition value.
                          For all the condition columns to be grouped together in the dataframe,
                          the dictionary key should have the prefix "condition_".
                          If condition is needed as condition per row, the public method `normalize_conditions_per_row`
                          can be provided as the callback function.
                          If condition value is needed as a string summary of condition data, the public method
                          `summarize_conditions_as_a_string` can be provided as this callback function.
                          If None is passed, conditions will not be included in the dataframe.

    Returns:
        A Pandas DataFrame with the each spec fields having a separate column.
        Following fields are split into sub-columns.
            - conditions: format of the condition columns are decided by the  `condition_format`
            argument of this function.
            - Properties: All the unique properties across all specs will be split into separate columns.
            For example, properties.property1, properties.property2, etc.
    """
    specs_dict = [
        __convert_spec_to_dict(spec=spec, condition=condition)
        for spec in specs
        for condition in (
            condition_format(spec.conditions)
            if (spec.conditions and condition_format)
            else [{}]
        )
    ]

    specs_dataframe = pd.json_normalize(specs_dict)
    specs_dataframe = __format_specs_columns(specs_dataframe=specs_dataframe)
    specs_dataframe.dropna(axis="columns", how="all", inplace=True)

    return specs_dataframe


def __convert_spec_to_dict(
    spec: Specification, condition: Dict[str, Any]
) -> Dict[str, Any]:
    """Converts a spec into dictionary.

    Args:
        spec: Spec object.
        condition: Condition as a dictionary which is added to the output spec dictionary.

    Returns:
        Spec as a dictionary with the provided condition dictionary included.
    """
    return {
        **{
            key: value
            for key, value in vars(spec).items()
            if key not in ["type", "limit", "conditions"]
        },
        **(__serialize_type(spec.type) if spec.type else {}),
        **(__serialize_limits(spec.limit) if spec.limit else {}),
        **{key: value for key, value in condition.items()},
    }


def __serialize_limits(limit: SpecificationLimit) -> Dict[str, str]:
    """Serialize limit into limit.min, limit.typical and limit.max.

    Args:
        limit: Limit of a spec.

    Returns:
        Limit as a dictionary.
    """
    return {f"limit.{key}": value for key, value in vars(limit).items()}


def __serialize_type(type: SpecificationType) -> Dict[str, str]:
    """Serialize type into it's string value.

    Args:
        type: Type of a spec.

    Returns:
        Type as a dictionary.
    """
    return {"type": type.name}


def __format_specs_columns(specs_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Format specs column to group conditions and keep properties and keywords at the end.

    Args:
        specs_dataframe: Dataframe of specs.

    Returns:
        Formatted dataframe of specs.
    """
    column_headers = specs_dataframe.columns.to_list()
    standard_column_headers = [
        header for header in column_headers if __is_standard_column_header(header)
    ]
    condition_headers = [
        header for header in column_headers if __is_condition_header(header=header)
    ]
    properties_headers = [
        header for header in column_headers if __is_property_header(header=header)
    ]
    formatted_column_headers = (
        standard_column_headers
        + condition_headers
        + (["keywords"] if "keywords" in column_headers else [])
        + properties_headers
    )

    return specs_dataframe.reindex(columns=formatted_column_headers, copy=False)


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

    return f"{DataFrameHeaders.CONDITION_COLUMN_HEADER_PREFIX}{name}{unit}"


def __serialize_condition_value(condition: Condition) -> List[str]:
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
        The list of ranges of the given condition where each range will be in
        string format `[min: <value>; max: <value>; step: <value>]` if the corresponding
        fields are not none.
    """
    if not value.range:
        return []

    return [
        f"""[{'; '.join(
            f'{range_key}: {range_value}'
            for range_key, range_value in vars(range).items()
            if range_value is not None
        )}]"""
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
