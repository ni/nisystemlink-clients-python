from typing import Callable, Dict, List, Optional, Union

import pandas as pd
from nisystemlink.clients.spec._spec_client import SpecClient
from nisystemlink.clients.spec.models._condition import (
    Condition,
    NumericConditionValue,
    StringConditionValue,
)
from nisystemlink.clients.spec.models._query_specs import (
    QuerySpecificationsRequest,
    QuerySpecificationsResponse,
    SpecificationProjection,
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
        f"[{'; '.join(f'{k}: {v}' for k, v in vars(range).items() if v is not None)}]"
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


def __format_specs_columns(specs_df: pd.DataFrame) -> pd.DataFrame:
    """Format specs column to group conditions and keep properties adn keywords at the end.

    Args:
        specs_df: Dataframe of specs.

    Returns:
        Formatted dataframe of specs.
    """
    column_headers = specs_df.columns.to_list()
    formatted_column_headers = [
        header
        for header in column_headers
        if not any(
            substring in header
            for substring in ["condition_", "properties.", "keywords"]
        )
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

    specs_df = specs_df.reindex(columns=formatted_column_headers)

    return specs_df


def __serialize_specs(
    specs: List[QuerySpecificationsResponse],
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

    specs_df = pd.json_normalize(specs_dict)
    specs_df = __format_specs_columns(specs_df=specs_df)
    specs_df.dropna(axis="columns", how="all", inplace=True)

    return specs_df


def __batch_query_specs(
    client: SpecClient,
    product_id: str,
    filter: Optional[str] = None,
    column_projection: Optional[List[SpecificationProjection]] = None,
) -> List[QuerySpecificationsResponse]:
    """Batch query specs of a specific product.

    Args:
        client: The Spec Client to use for the request.
        product_ids: ID of the product to query specs.
        filter: The specification query filter in Dynamic Linq format.
        column_projection: List of columns to be included to the spec dataframe.
                           This is an optional parameter. By default all the values will be retrieved.

    Returns:
        The list of specs of the specified product.
    """
    query_request = QuerySpecificationsRequest(
        product_ids=[product_id], take=1000, filter=filter, projection=column_projection
    )
    spec_response = client.query_specs(query_request)
    specs = []

    if spec_response.specs:
        specs = spec_response.specs

    while spec_response.continuation_token:
        query_request.continuation_token = spec_response.continuation_token
        spec_response = client.query_specs(query_request)

        if spec_response.specs:
            specs.extend(spec_response.specs)

    return specs


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
        filter=filter,
        column_projection=column_projection,
    )
    should_not_format_condition = column_projection and (
        SpecificationProjection.CONDITION_NAME not in column_projection
        or SpecificationProjection.CONDITION_VALUES not in column_projection
    )
    specs_df = __serialize_specs(
        specs=specs,
        condition_format=None if should_not_format_condition else condition_format,
    )

    return specs_df
