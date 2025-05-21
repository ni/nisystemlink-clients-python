import enum
from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class TestPlanTemplateOrderBy(str, Enum):
    """An enumeration by which test plan templates can be ordered/sorted."""

    ID = enum.auto()
    NAME = enum.auto()
    TEMPLATE_GROUP = enum.auto()
    CREATED_AT = enum.auto()
    UPDATED_AT = enum.auto()


class TestPlanTemplateField(str, Enum):
    ID = enum.auto()
    NAME = enum.auto()
    TEMPLATE_GROUP = enum.auto()
    PRODUCT_FAMILIES = enum.auto()
    PART_NUMBERS = enum.auto()
    SUMMARY = enum.auto()
    DESCRIPTION = enum.auto()
    TEST_PROGRAM = enum.auto()
    ESTIMATED_DURATION_IN_SECONDS = enum.auto()
    SYSTEM_FILTER = enum.auto()
    EXECUTION_ACTIONS = enum.auto()
    FILE_IDS = enum.auto()
    WORKSPACE = enum.auto()
    PROPERTIES = enum.auto()
    DASHBOARD = enum.auto()
    CREATED_BY = enum.auto()
    UPDATED_BY = enum.auto()
    CREATED_AT = enum.auto()
    UPDATED_AT = enum.auto()


class QueryTestPlanTemplatesRequest(JsonModel):
    """Request information for the query test plan templates API."""

    filter: Optional[str] = None
    """The test plan template query filter in dynamic LINQ format.

    `id`: String representing the ID of a test plan template. Field supports only equals '=' and not
    equal '!=' operators for filtering.
    `productFamilies`: Array of strings representing the product families to which the test plan
    template belongs.
    `partNumbers`: Array of strings representing the part numbers of the products to which the test
    plan template belongs.
    `fileIds`: The array of file IDs associated with the test plan template.
    `name`: String representing the name of a test plan template.
    `summary`: String representing the summary of a test plan template.
    `description`: String representing description of the test plan created from this template.
    `templateGroup`: String representing the template group defined by the user.
    `testProgram`: String representing the test program name of the test plan created from this
    template.
    `systemFilter`: String representing the LINQ filter used to filter the potential list of systems
    capable of executing test plans created from this template.
    `workspace`: String representing the workspace where the test plan template belongs.
    `createdBy`: String representing the user who created the test plan template.
    `updatedBy`: String representing the user who updated the test plan template.
    `createdAt`: ISO-8601 formatted timestamp indicating when the test plan template was created.
    `updatedAt`: ISO-8601 formatted timestamp indicating when the test plan template was most
    recently updated.
    `properties`: Collection of key-value pairs related to a test plan created from this template.
    Example: properties.Any(key == "Location" & value == "Austin")

    See [Dynamic Linq](https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language)
    documentation for more details.

    `"@0"`, `"@1"` etc. can be used in conjunction with the `substitutions` parameter to keep this
    query string more simple and reusable."""

    take: Optional[int] = None
    """The maximum number of test plan templates to return."""

    order_by: Optional[TestPlanTemplateOrderBy] = None
    """Field by which test plan templates can be ordered/sorted."""

    substitutions: Optional[List[str]] = None
    """Makes substitutions in the query filter expression
    using non-negative integers. These integers
    use the @ symbol as a prefix. The filter
    expression replaces each substitution
    with the element at the corresponding
    index in this list. The index is zero-based."""

    descending: Optional[bool] = None
    """Whether to return the test plan templates in the descending order. By default, test plan
    templates are sorted in the ascending order."""

    continuation_token: Optional[str] = None
    """Allows users to continue the query at the next test plan templates that matches the given
    criteria."""

    projection: List[TestPlanTemplateField] = []
    """
    Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """

    """
    To retrieve the next page of test plan templates, pass the continuation token from the previous
    page in the next request. The service responds with the next page of data and provides a new
    continuation token. To paginate results, continue sending requests with the newest continuation
    token provided in each response.
    """


class _QueryTestPlanTemplatesRequest(JsonModel):
    """Request information for the query test plan templates API."""

    filter: Optional[str] = None
    """The test plan template query filter in dynamic LINQ format.

    `id`: String representing the ID of a test plan template. Field supports only equals '=' and not
    equal '!=' operators for filtering.
    `productFamilies`: Array of strings representing the product families to which the test plan
    template belongs.
    `partNumbers`: Array of strings representing the part numbers of the products to which the test
    plan template belongs.
    `fileIds`: The array of file IDs associated with the test plan template.
    `name`: String representing the name of a test plan template.
    `summary`: String representing the summary of a test plan template.
    `description`: String representing description of the test plan created from this template.
    `templateGroup`: String representing the template group defined by the user.
    `testProgram`: String representing the test program name of the test plan created from this
    template.
    `systemFilter`: String representing the LINQ filter used to filter the potential list of systems
    capable of executing test plans created from this template.
    `workspace`: String representing the workspace where the test plan template belongs.
    `createdBy`: String representing the user who created the test plan template.
    `updatedBy`: String representing the user who updated the test plan template.
    `createdAt`: ISO-8601 formatted timestamp indicating when the test plan template was created.
    `updatedAt`: ISO-8601 formatted timestamp indicating when the test plan template was most
    recently updated.
    `properties`: Collection of key-value pairs related to a test plan created from this template.
    Example: properties.Any(key == "Location" & value == "Austin")

    See
    [Dynamic Linq](https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language)
    documentation for more details.

    `"@0"`, `"@1"` etc. can be used in conjunction with the `substitutions` parameter to keep this
    query string more simple and reusable.
    """

    take: Optional[int] = None
    """The maximum number of test plan templates to return."""

    order_by: Optional[TestPlanTemplateOrderBy] = None
    """Field by which test plan templates can be ordered/sorted."""

    substitutions: Optional[List[str]] = None
    """Makes substitutions in the query filter expression
    using non-negative integers. These integers
    use the @ symbol as a prefix. The filter
    expression replaces each substitution
    with the element at the corresponding
    index in this list. The index is zero-based."""

    descending: Optional[bool] = None
    """Whether to return the test plan templates in the descending order. By default, test plan
    templates are sorted in the ascending order."""

    continuation_token: Optional[str] = None
    """Allows users to continue the query at the next test plan templates that matches the given
    criteria."""

    projection: Optional[List[str]] = None
    """
    Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """
