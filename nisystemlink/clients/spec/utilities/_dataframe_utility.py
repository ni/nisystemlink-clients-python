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
    SpecificationWithOptionalFields,
)


def __generate_column_header(condition: Condition) -> str:
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


def __serialize_numeric_range(value: NumericConditionValue) -> List[str]:
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


def __serialize_discrete_values(
    value: Union[NumericConditionValue, StringConditionValue]
) -> List[str]:
    """Serialize discrete values of a value.

    Args:
        value: A condition's value with either NumericConditionValue type or StringConditionValue type.

    Returns:
        The list of discrete values of the given value in a specific format.
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
        values.extend(__serialize_numeric_range(value=condition.value))

    values.extend(__serialize_discrete_values(value=condition.value))

    return values


def __serialize_conditions(conditions: List[Condition]) -> Dict[str, str]:
    """Serialize conditions into desired format.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a dictionary in specific format for the dataframe.
    """
    return {
        __generate_column_header(condition): ", ".join(
            __get_condition_values(condition)
        )
        for condition in conditions
    }


def __serialize_specs(
    specs: List[SpecificationWithOptionalFields],
    condition_format: Callable[[List[Condition]], Dict],
) -> pd.DataFrame:
    """Format specs of with respect to the provided condition format.

    Args:
        specs: List of specs of the specified product.
        condition_format: Function with which conditions columns and condition values are formatted.

    Returns:
        The list of specs of the specified product as a dataframe.
    """
    specs_dict = [
        {
            **{key: value for key, value in vars(spec).items() if key != "conditions"},
            **(condition_format(spec.conditions) if spec.conditions else {}),
        }
        for spec in specs
    ]

    specs_df = pd.json_normalize(specs_dict)
    specs_df = specs_df.loc[
        :, specs_df.apply(lambda col: any(val is not None for val in col))
    ]

    return specs_df


def __batch_query_specs(
    client: SpecClient,
    product_id: str,
    column_projection: Optional[List[str]] = None,
) -> List[SpecificationWithOptionalFields]:
    """Batch query specs of a specific product.

    Args:
        client: The Spec Client to use for the request.
        product_ids: ID od the product to query specs.
        column_projection: List of columns to be included to the spec dataframe
                           Every column will be included if column_projection is 'None'.

    Returns:
        The list of specs of the specified product.
    """
    query_request = QuerySpecificationsRequest(
        product_ids=[product_id], take=1000, projection=column_projection
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
    column_projection: Optional[List[str]] = None,
    condition_format: Callable[
        [List[Condition]], Dict[str, str]
    ] = __serialize_conditions,
) -> pd.DataFrame:
    """Get specs of a specific product as a dataframe.

    Args:
        client: The Spec Client to use for the request.
        product_ids: ID od the product to query specs.
        column_projection: List of columns to be included to the spec dataframe
                           Every column will be included if column_projection is 'None'.
        condition_format: Function with which conditions columns and condition values are formatted.

    Returns:
        The list of specs of the specified product as a dataframe.
    """
    specs = __batch_query_specs(
        client=client, product_id=product_id, column_projection=column_projection
    )
    specs_df = __serialize_specs(specs=specs, condition_format=condition_format)

    return specs_df
