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
    column_header = (
        "condition_"
        + (condition.name if condition.name else "")
        + (
            f"({condition.value.unit})"
            if type(condition.value) == NumericConditionValue and condition.value.unit
            else ""
        )
    )

    return column_header


def __serialize_numeric_range(value: NumericConditionValue) -> List[str]:
    """Serialize ranges of a numeric condition value.

    Args:
        value: A condition's value with NumericConditionValue type.

    Returns:
        The list of ranges of the given value in a specific format.
    """
    ranges = []

    for range in value.range or []:
        ranges.append(
            f"[{'; '.join([f'{k}: {v}' for k, v in vars(range).items() if v is not None])}]"
        )

    return ranges


def _serialize_discrete_values(
    value: Union[NumericConditionValue, StringConditionValue]
) -> List[str]:
    """Serialize discrete values of a value.

    Args:
        value: A condition's value with either NumericConditionValue type or StringConditionValue type.

    Returns:
        The list of discrete values of the given value in a specific format.
    """
    return [str(discrete) for discrete in value.discrete or []]


def __get_condition_values(condition: Condition) -> List[str]:
    """Get ranges and discrete values of a condition.

    Args:
        condition: Condition for getting values.

    Returns:
        The list of values of the given condition in a specific format.
    """
    values = []

    if condition.value:
        if type(condition.value) == NumericConditionValue:
            ranges = __serialize_numeric_range(value=condition.value)
            values.extend(ranges)

        discrete_values = _serialize_discrete_values(value=condition.value)
        values.extend(discrete_values)

    return values


def __serialize_conditions(conditions: List[Condition]) -> Dict:
    """Seriazlize conditions into desired format.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a dictionary in specific format for the dataframe.
    """
    condition_dict = {}

    for condition in conditions:
        column_header = __generate_column_header(condition=condition)
        values = __get_condition_values(condition=condition)
        condition_dict[column_header] = ", ".join(values)

    return condition_dict


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
    specs_dict = []

    for spec in specs:
        spec_dict = vars(spec)

        if spec.conditions:
            condition_dict = condition_format(spec.conditions)

            spec_dict.pop("conditions")
            spec_dict.update(condition_dict)

        specs_dict.append(spec_dict)

    specs_df = pd.json_normalize(specs_dict)
    specs_df = specs_df.loc[
        :, specs_df.apply(lambda col: any(val is not None for val in col))
    ]

    return specs_df


def get_specs_dataframe(
    client: SpecClient,
    product_id: str,
    column_projection: Optional[List[str]] = None,
    condition_format: Callable[[List[Condition]], Dict] = __serialize_conditions,
) -> pd.DataFrame:
    """Query specs of a specific product.

    Args:
        client: The Spec Client to use for the request.
        product_ids: ID od the product to query specs.
        column_projection: List of columns to be included to the spec dataframe
                           Every column will be included if column_projection is 'None'.
        condition_format: Function with which conditions columns and condition values are formatted.

    Returns:
        The list of specs of the specified product as a dataframe.
    """
    spec_response = client.query_specs(
        QuerySpecificationsRequest(
            product_ids=[product_id], take=1000, projection=column_projection
        )
    )
    specs = spec_response.specs if spec_response.specs else []

    while spec_response.continuation_token:
        continuation_token = spec_response.continuation_token
        spec_response = client.query_specs(
            QuerySpecificationsRequest(
                product_ids=[product_id],
                take=1000,
                continuation_token=continuation_token,
                projection=column_projection,
            )
        )

        specs.extend(spec_response.specs if spec_response.specs else [])

    specs_df = __serialize_specs(specs=specs, condition_format=condition_format)
    return specs_df
