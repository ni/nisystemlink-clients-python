from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.core._uplink._with_paging import WithPaging
from nisystemlink.clients.spec.models._specification import Specification


class SpecificationProjection(str, Enum):
    """The allowed projections for query.

    When using projection, only the fields specified by the projection element will be included in
    the response.
    """

    ID = "ID"
    PRODUCT_ID = "PRODUCT_ID"
    SPEC_ID = "SPEC_ID"
    NAME = "NAME"
    CATEGORY = "CATEGORY"
    TYPE = "TYPE"
    SYMBOL = "SYMBOL"
    BLOCK = "BLOCK"
    LIMIT = "LIMIT"
    UNIT = "UNIT"
    CONDITION_NAME = "CONDITION_NAME"
    CONDITION_VALUES = "CONDITION_VALUES"
    CONDITION_UNIT = "CONDITION_UNIT"
    CONDITION_TYPE = "CONDITION_TYPE"
    KEYWORDS = "KEYWORDS"
    PROPERTIES = "PROPERTIES"
    WORKSPACE = "WORKSPACE"
    CREATED_AT = "CREATED_AT"
    CREATED_BY = "CREATED_BY"


class SpecificationOrderBy(Enum):
    """The valid ways to order the response to a spec query."""

    ID = "ID"
    SPEC_ID = "SPEC_ID"


class QuerySpecificationsRequest(JsonModel):
    """The request to query specifications."""

    product_ids: List[str]
    """IDs of the products to query the specifications for."""

    take: Optional[int] = None
    """Maximum number of specifications to return in the current API response.

    Uses the default if the specified value is negative. The default value is `1000` specs.
    """

    continuation_token: Optional[str] = None
    """Allows users to continue the query at the next specification that matches the given criteria.

    To retrieve the next batch of specifications, pass the continuation token from the previous
    batch in the next request. The service responds with the next batch of data and provides a new
    continuation token. To paginate results, continue sending requests with the newest continuation
    token provided in each response.
    """

    filter: Optional[str] = None
    """
    The specification query filter in Dynamic Linq format.

    Allowed properties in the filter are:
    - `specId`: String representing the SpecID of a specification.
    - `name`: String representing the name of a specification.
    - `category`: String representing the category of a specification.
    - `type`: String enumeration representing the type of the specification.
        Possible values are : PARAMETRIC, FUNCTIONAL
    - `block`: String representing the block of a specification.
    - `symbol`: String representing the symbol of a specification.
    - `unit`: String representing the unit of a specification.
    - `workspace`: String representing the ID of the workspace the specification belongs to.
    - `createdBy`: String representing the ID of the user who created the specification.
    - `createdAt`: ISO-8601 formatted UTC timestamp indicating when the specification was created.
    - `updatedBy`: String representing the ID of the user who updated the specification.
    - `updatedAt`: ISO-8601 formatted UTC timestamp indicating when the specification was updated.

    See [Dynamic Linq](https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language)
    documentation for more details.
    """

    projection: Optional[List[SpecificationProjection]] = None
    """Specifies the fields to include in the returned specifications.

    Fields you do not specify are excluded. Returns all fields if no value is specified.
    """

    order_by: Optional[SpecificationOrderBy] = None
    """Specifies the field to use to sort specifications.

    By default, specifications are sorted by `ID`.
    """
    order_by_descending: Optional[bool] = None
    """Specifies whether to return the specifications in descending order.

    By default, this value is `false` and specifications are sorted in ascending order.
    """


class PagedSpecifications(WithPaging):
    """The list of matching specifications and a continuation token to get the next items."""

    specs: Optional[List[Specification]] = None
    """List of queried specifications.

    An empty list indicates that there are no specifications meeting the criteria provided in the
    request.
    """
