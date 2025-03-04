from typing import Callable, Dict, List, Optional, Union

import pandas as pd
from nisystemlink.clients.spec._spec_client import SpecClient
from nisystemlink.clients.spec.models._condition import (
    Condition,
    NumericConditionValue,
    StringConditionValue,
)
from nisystemlink.clients.spec.models._query_specs import (
    SpecificationProjection,
)
from nisystemlink.clients.spec.models._specification import Specification
from nisystemlink.clients.spec.utilities._client_utilities import __batch_query_specs
from nisystemlink.clients.spec.utilities._constants import (
    CONDITION_COLUMN_HEADER,
    KEYWORDS_COLUMN_HEADER,
    PROPERTY_COLUMN_HEADER,
)


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
    }


def get_specs_dataframe(
    client: SpecClient,
    product_id: str,
    filter: Optional[str] = None,
    column_projection: Optional[List[SpecificationProjection]] = None,
    condition_format: Callable[
        [List[Condition]], Dict[str, str]
    ] = __serialize_conditions,
) -> pd.DataFrame:
    """Get specs of a specific product as a dataframe.

    Args:
        client: The Spec Client to use for the request.
        product_ids: ID of the product to query specs.
        filter: The specification query filter in Dynamic Linq format.
        column_projection: List of columns to be included to the spec dataframe.
                           This is an optional parameter. By default all the values will be retrieved.
        condition_format: Function which takes in a list of condition objects and returns
                          a dictionary of condition and its values. The dictionary keys
                          should be the condition name and the values should be the condition
                          value in any format you need. Keys will be used as the dataframe
                          column header and values will be used as the row cells for the
                          respective column header. For all the condition columns to be grouped
                          together in the dataframe, the dictionary key should have the prefix "condition_".
                          This is an optional parameter. By default column header will be
                          "condition_<conditionName>(<conditionUnit>)".
                          The column value will be "[min: num; max: num, step: num], num, num"
                          where data within the '[]' is numeric condition range and other num
                          values are numeric condition discrete values.
                          The column value will be "str, str, str" - where str values are the
                          condition discrete values for a string condition.

    Returns:
        The list of specs of the specified product as a dataframe.

    Raises:
        ApiException: if unable to communicate with the `/nispec` service or if there are
        invalid arguments.
    """
    specs = __batch_query_specs(
        client=client,
        product_id=product_id,
        take=1000,
        filter=filter,
        column_projection=column_projection,
    )
    specs_dataframe = __serialize_specs(
        specs=specs,
        condition_format=(
            condition_format
            if __allow_condition_format(column_projection=column_projection)
            else None
        ),
    )

    return specs_dataframe


def __allow_condition_format(
    column_projection: Optional[List[SpecificationProjection]] = None,
) -> bool:
    """Check if condition fomatting can be allowed.

    Args:
        column_projection: List of columns to be included to the spec dataframe.

    Returns:
        True if either column projection is None or column projection is not empty
        or condition name or condition values is not included in column projection.
    """
    return (not column_projection) or (
        len(column_projection) > 0
        and (
            SpecificationProjection.CONDITION_NAME in column_projection
            and SpecificationProjection.CONDITION_VALUES in column_projection
        )
    )


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
            for range_key, range_value in vars(r).items()
            if range_value is not None
        )}]"
        for r in value.range
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


def __is_condition_header(header: str) -> bool:
    """Check if column header is not a condition.

    Args:
        header: column header for specs dataframe.

    Returns:
        True if header contians 'condition_'. Else returns false.

    """
    return CONDITION_COLUMN_HEADER in header


def __is_property_header(header: str) -> bool:
    """Check if column header is not a property.

    Args:
        header: column header for specs dataframe.

    Returns:
        True if header contians 'properties.'. Else returns false.

    """
    return PROPERTY_COLUMN_HEADER in header


def __is_keywords_header(header: str) -> bool:
    """Check if column header is not a keywords.

    Args:
        header: column header for specs dataframe.

    Returns:
        True if header contians 'keywords'. Else returns false.

    """
    return KEYWORDS_COLUMN_HEADER in header


def __is_allowed_headers(header: str) -> bool:
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


def __format_specs_columns(specs_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Format specs column to group conditions and keep properties and keywords at the end.

    Args:
        specs_dataframe: Dataframe of specs.

    Returns:
        Formatted dataframe of specs.
    """
    column_headers = specs_dataframe.columns.to_list()
    formatted_column_headers = [
        header for header in column_headers if __is_allowed_headers(header)
    ]
    condition_headers = [header for header in column_headers if "condition_" in header]
    properties_headers = [
        header for header in column_headers if "properties." in header
    ]
    formatted_column_headers += (
        condition_headers
        + properties_headers
        + (["keywords"] if "keywords" in column_headers else [])
    )

    return specs_dataframe.reindex(columns=formatted_column_headers)


def __serialize_specs(
    specs: List[Specification],
    condition_format: Optional[Callable[[List[Condition]], Dict]] = None,
) -> pd.DataFrame:
    """Format specs with respect to the provided condition format.

    Args:
        specs: List of specs of the specified product.
        condition_format: Function which takes in a list of condition objects and returns
                          a dictionary of condition and its values. The dictionary keys
                          should be the condition name and the values should be the condition
                          value in any format you need. Keys will be used as the dataframe
                          column header and values will be used as the row cells for the
                          respective column header. For all the condition columns to be grouped
                          together in the dataframe, the dictionary key should have the prefix "condition_".
                          This is an optional parameter. By default column header will be
                          "condition_<conditionName>(<conditionUnit>)".
                          The column value will be "[min: num; max: num, step: num], num, num"
                          where data within the '[]' is numeric condition range and other num
                          values are numeric condition discrete values.
                          The column value will be "str, str, str" - where str values are the
                          condition discrete values for a string condition.

    Returns:
        The list of specs of the specified product as a dataframe.
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
