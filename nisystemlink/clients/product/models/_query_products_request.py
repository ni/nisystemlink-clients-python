from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class ProductOrderBy(str, Enum):
    """The valid ways to order a product query."""

    ID = "ID"
    FAMILY = "FAMILY"
    PART_NUMBER = "PART_NUMBER"
    NAME = "NAME"
    UPDATED_AT = "UPDATED_AT"


class ProductField(str, Enum):
    """An enumeration of product fields for which the values can be queried for."""

    ID = "ID"
    FAMILY = "FAMILY"
    PART_NUMBER = "PART_NUMBER"
    NAME = "NAME"
    UPDATED_AT = "UPDATED_AT"


class ProductProjection(str, Enum):
    """An enumeration of all fields in a Product. These are used to project the required fields
    from the API response.
    """

    ID = "ID"
    FAMILY = "FAMILY"
    PART_NUMBER = "PART_NUMBER"
    NAME = "NAME"
    UPDATED_AT = "UPDATED_AT"
    WORKSPACE = "WORKSPACE"
    KEYWORDS = "KEYWORDS"
    PROPERTIES = "PROPERTIES"
    FILE_IDS = "FILE_IDS"


class QueryProductsBase(JsonModel):
    filter: Optional[str] = None
    """
    The product query filter in Dynamic Linq format.

    Allowed properties in the filter are:
    - `id`: String for the global identifier of the product
    - `partNumber`: String representing the part number of the product
    - `name`: String of the product name
    - `family`: String for the product family
    - `updatedAt`: ISO-8601 formatted UTC timestamp indicating when the product was last updated.
    - `keywords`: A list of keyword strings
    - `properties`: A dictionary of additional string to string properties
    - `fileIds`: A list of string ids for files stored in the file service (`/nifile`)

    See [Dynamic Linq](https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language)
    documentation for more details.

    `"@0"`, `"@1"` etc. can be used in conjunction with the `substitutions` parameter to keep this
    query string more simple and reusable.
    """

    substitutions: Optional[List[str]] = None
    """String substitutions into the `filter`.

    Makes substitutions in the query filter expression. Substitutions for the query expression are
    indicated by non-negative integers that are prefixed with the "at" symbol. Each substitution in
    the given expression will be replaced by the element at the corresponding index (zero-based) in
    this list. For example, "@0" in the filter expression will be replaced with the element at the
    zeroth index of the substitutions list.
    """


class QueryProductsRequest(QueryProductsBase):

    order_by: Optional[ProductOrderBy] = Field(None, alias="orderBy")
    """Specifies the fields to use to sort the products.

    By default, products are sorted by `id`
    """

    descending: Optional[bool] = None
    """Specifies whether to return the products in descending order.

    By default, this value is `false` and products are sorted in ascending order.
    """

    projection: Optional[List[ProductProjection]] = None
    """Specifies the product fields to project.

    When a field value is given here, the corresponding field will be present in all returned products,
    and all unspecified fields will be excluded. If no projection is specified, all product fields
    will be returned.
    """

    take: Optional[int] = None
    """Maximum number of products to return in the current API response.

    Uses the default if the specified value is negative. The default value is `1000` products.
    """

    continuation_token: Optional[str] = None
    """Allows users to continue the query at the next product that matches the given criteria.

    To retrieve the next page of products, pass the continuation token from the previous
    page in the next request. The service responds with the next page of data and provides a new
    continuation token. To paginate results, continue sending requests with the newest continuation
    token provided in each response.
    """

    return_count: Optional[bool] = None
    """If true, the response will include a count of all products matching the filter.

    By default, this value is `False` and count is not returned. Note that returning the count may
    incur performance penalties as the service may have to do a complete walk of the database to
    compute count. """


class QueryProductValuesRequest(QueryProductsBase):
    field: Optional[ProductField] = None
    """The product field to return for this query."""

    starts_with: Optional[str] = None
    """Only return string parameters prefixed by this value (case sensitive)."""
