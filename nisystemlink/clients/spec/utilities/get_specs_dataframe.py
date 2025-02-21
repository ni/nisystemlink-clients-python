from typing import Callable, Dict, List, Optional
import pandas as pd

from nisystemlink.clients.spec._spec_client import SpecClient
from nisystemlink.clients.spec.models._condition import Condition, NumericConditionValue
from nisystemlink.clients.spec.models._query_specs import Projection, QuerySpecificationsRequest


def __serialize_conditions(conditions: List[Condition]) -> Dict:
    """Seriazlize conditions into desired format.

    Args:
        conditions: List of all conditions in a spec.

    Returns:
        Conditions as a dictionary in specific format for the dataframe.
    """
    condition_dict = {}

    for condition in conditions:
        column_header = (
            "condition_" + 
            (
                condition.name
                if condition.name
                else ""
            ) +
            (
                f"({condition.value.unit})"
                if type(condition.value) == NumericConditionValue and condition.value.unit
                else ""
            )
        )

        condition_dict[column_header] = ""

        values = []

        if condition.value:
            if type(condition.value) == NumericConditionValue:
                for range in condition.value.range or []:
                    values.append(
                        f"[{'; '.join([f'{k}: {v}' for k, v in vars(range).items() if v is not None])}]"
                    )

            values.extend(
                [str(discrete) for discrete in condition.value.discrete or []]
            )

        condition_dict[column_header] = ", ".join(values)

    return condition_dict


def get_specs_dataframe(client: SpecClient, product_id: str, column_projection: Optional[List[str]] = None, condition_format: Callable[[List[Condition]], Dict] = __serialize_conditions) -> pd.DataFrame:
    """Query specs of a specific product.

    Args:
        client: The Spec Client to use for the request.
        product_ids: ID od the product to query specs.

    Returns:
        The list of specs of the specified product.
    """
    spec_response = client.query_specs(
        QuerySpecificationsRequest(
            product_ids=[product_id],
            take=1000,
            projection=column_projection
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
                projection=column_projection
            )
        )

        specs.extend(spec_response.specs if spec_response.specs else [])

    specs_dict = []

    for spec in specs:
        spec_dict = vars(spec)

        if not column_projection or "conditions" in column_projection:
            condition_dict = condition_format(spec.conditions)

            spec_dict.pop("conditions")
            spec_dict.update(condition_dict)

        specs_dict.append(spec_dict)

    specs_df = pd.json_normalize(specs_dict)
    return specs_df
