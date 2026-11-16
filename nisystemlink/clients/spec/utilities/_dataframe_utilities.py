from typing import Any, Callable, Dict, List

import pandas as pd
from nisystemlink.clients.spec.models._condition import (
    Condition,
    NumericConditionValue,
    StringConditionValue,
)
from nisystemlink.clients.spec.models._specification import (
    MeasurementMappingItem,
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


def summarize_measurement_mappings_as_a_string(
    measurement_mappings: List[MeasurementMappingItem],
) -> List[Dict[str, str]]:
    """Converts the measurement mappings to an easily readable string format.

    Args:
        measurement_mappings: List of all measurement mappings in a spec.

    Returns:
        A list with a single dictionary. The key will be "measurement_mapping" and the value
        will be "[filter: <value>; result_filter: <value>], [filter: <value>]" where each
        bracketed group is a mapping item. Fields that are None are left out and items
        without any field are skipped. The list is empty if there is nothing to summarize.
    """
    summaries = []
    for item in measurement_mappings:
        fields = __serialize_measurement_mapping_fields(item)
        if fields:
            summaries.append(
                "["
                + "; ".join(f"{key}: {value}" for key, value in fields.items())
                + "]"
            )

    return [{"measurement_mapping": ", ".join(summaries)}] if summaries else []


def normalize_measurement_mappings_per_column(
    measurement_mappings: List[MeasurementMappingItem],
) -> List[Dict[str, Any]]:
    """Convert measurement mappings into a single dictionary where each mapping item is
    split into indexed keys.

    Args:
        measurement_mappings: List of all measurement mappings in a spec.

    Returns:
        A list with a single dictionary. The keys will be
        "measurement_mapping[<index>].filter" and "measurement_mapping[<index>].result_filter"
        and the values will be the corresponding mapping item field. Fields that are None
        are left out. The list is empty if no mapping item has a value.
    """
    columns = {
        f"measurement_mapping[{index}].{key}": value
        for index, item in enumerate(measurement_mappings)
        for key, value in __serialize_measurement_mapping_fields(item).items()
    }

    return [columns] if columns else []


def normalize_measurement_mappings_per_row(
    measurement_mappings: List[MeasurementMappingItem],
) -> List[Dict[str, Any]]:
    """Convert measurement mappings into list of dictionaries where dictionary keys will be
    'measurement_mapping.filter' and 'measurement_mapping.result_filter'.

    Args:
        measurement_mappings: List of all measurement mappings in a spec.

    Returns:
        A list of dictionaries, one for each mapping item that has a value. Fields that
        are None are left out. Each mapping item will be logged as separate dictionary
        entry in the list which translates to separate row in the dataframe.
    """
    return [
        {f"measurement_mapping.{key}": value for key, value in fields.items()}
        for fields in (
            __serialize_measurement_mapping_fields(item)
            for item in measurement_mappings
        )
        if fields
    ]


def convert_specs_to_dataframe(
    specs: List[Specification],
    condition_format: (
        Callable[[List[Condition]], List[Dict[str, Any]]] | None
    ) = normalize_conditions_per_column,
    measurement_mapping_format: (
        Callable[[List[MeasurementMappingItem]], List[Dict[str, Any]]] | None
    ) = normalize_measurement_mappings_per_column,
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
        measurement_mapping_format: A callback function which takes in a list of measurement mapping
                          items of a spec and returns a list of dictionary of measurement mapping
                          data. Dataframe rows will be constructed based on these list of
                          dictionaries. Each dictionary in the list indicates a row. If there is
                          more than one dictionary in the list, it will be considered as a new
                          row and other spec column data will be duplicated. Keys will be used as
                          the dataframe column header and values will be used as the row cells
                          for the respective column header.
                          If not passed, each mapping item will be split into the indexed columns
                          `measurement_mapping[<index>].filter` and
                          `measurement_mapping[<index>].result_filter`.
                          If measurement mapping is needed as one row per mapping item, the public
                          method `normalize_measurement_mappings_per_row` can be provided as the
                          callback function.
                          If measurement mapping is needed as a string summary, the public method
                          `summarize_measurement_mappings_as_a_string` can be provided as this
                          callback function.
                          If None is passed, measurement mappings will not be included in the dataframe.

    Returns:
        A Pandas DataFrame with the each spec fields having a separate column.
        Following fields are split into sub-columns.
            - conditions: format of the condition columns are decided by the  `condition_format`
            argument of this function.
            - measurement_mapping: format of the measurement mapping columns are decided by the
            `measurement_mapping_format` argument of this function.
            - Properties: All the unique properties across all specs will be split into separate columns.
            For example, properties.property1, properties.property2, etc.
    """
    specs_dict = [
        __convert_spec_to_dict(
            spec=spec,
            condition=condition,
            measurement_mapping=measurement_mapping,
        )
        for spec in specs
        for condition in (
            condition_format(spec.conditions)
            if (spec.conditions and condition_format)
            else [{}]
        )
        for measurement_mapping in (
            (measurement_mapping_format(spec.measurement_mapping) or [{}])
            if (spec.measurement_mapping and measurement_mapping_format)
            else [{}]
        )
    ]

    specs_dataframe = pd.json_normalize(specs_dict)
    specs_dataframe = __format_specs_columns(specs_dataframe=specs_dataframe)
    specs_dataframe.dropna(axis="columns", how="all", inplace=True)

    return specs_dataframe


def __convert_spec_to_dict(
    spec: Specification,
    condition: Dict[str, Any],
    measurement_mapping: Dict[str, Any],
) -> Dict[str, Any]:
    """Converts a spec into dictionary.

    Args:
        spec: Spec object.
        condition: Condition as a dictionary which is added to the output spec dictionary.
        measurement_mapping: Measurement mapping as a dictionary which is added to the output spec dictionary.

    Returns:
        Spec as a dictionary with the provided condition and measurement mapping dictionaries included.
    """
    return {
        **{
            key: value
            for key, value in vars(spec).items()
            if key not in ["type", "limit", "conditions", "measurement_mapping"]
        },
        **(__serialize_type(spec.type) if spec.type else {}),
        **(__serialize_limits(spec.limit) if spec.limit else {}),
        **{key: value for key, value in measurement_mapping.items()},
        **{key: value for key, value in condition.items()},
    }


def __serialize_measurement_mapping_fields(
    measurement_mapping: MeasurementMappingItem,
) -> Dict[str, str]:
    """Get the fields of a measurement mapping item that have a value.

    Args:
        measurement_mapping: Measurement mapping item of a spec.

    Returns:
        Dictionary with the keys "filter" and "result_filter" when their values are not None.
    """
    return {
        key: value
        for key, value in (
            ("filter", measurement_mapping.filter),
            ("result_filter", measurement_mapping.result_filter),
        )
        if value is not None
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
        "["
        + "; ".join(
            f"{range_key}: {range_value}"
            for range_key, range_value in vars(value_range).items()
            if range_value is not None
        )
        + "]"
        for value_range in value.range
    ]


def __serialize_condition_discrete_values(
    value: NumericConditionValue | StringConditionValue,
) -> List[str]:
    """Serialize discrete values of a value.

    Args:
        value: A condition's value with either NumericConditionValue type or StringConditionValue type.

    Returns:
        The list of discrete values of the given value in a string format.
    """
    return [str(discrete) for discrete in (value.discrete or [])]
