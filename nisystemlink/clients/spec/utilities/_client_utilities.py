from typing import List, Optional

from nisystemlink.clients.spec._spec_client import SpecClient
from nisystemlink.clients.spec.models._query_specs import (
    QuerySpecificationsRequest,
    SpecificationProjection,
)
from nisystemlink.clients.spec.models._specification import Specification
from nisystemlink.clients.spec.utilities._constants import DEFAULT_QUERY_SPECS_TAKE


def __batch_query_specs(
    client: SpecClient,
    product_id: str,
    take: Optional[int] = DEFAULT_QUERY_SPECS_TAKE,
    filter: Optional[str] = None,
    column_projection: Optional[List[SpecificationProjection]] = None,
) -> List[Specification]:
    """Batch query specs of a specific product.

    Args:
        client: The Spec Client to use for the request.
        product_ids: ID of the product to query specs.
        take: Maximum number of specifications to return in the current API response.
              The default value is 1000 specs.
              Uses the default if the specified value is negative.
        filter: The specification query filter in Dynamic Linq format.
        column_projection: List of columns to be included to the spec dataframe.
                           This is an optional parameter. By default all the values will be retrieved.

    Returns:
        The list of specs of the specified product.
    """
    query_request = QuerySpecificationsRequest(
        product_ids=[product_id],
        take=DEFAULT_QUERY_SPECS_TAKE,
        filter=filter,
        projection=column_projection,
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
