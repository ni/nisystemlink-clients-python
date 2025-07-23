from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging


class TestPlanTemplateOrderBy(str, Enum):
    """An enumeration by which test plan templates can be ordered/sorted."""

    ID = "ID"
    NAME = "NAME"
    TEMPLATE_GROUP = "TEMPLATE_GROUP"
    CREATED_AT = "CREATED_AT"
    UPDATED_AT = "UPDATED_AT"


class TestPlanTemplateField(str, Enum):
    """Model for an object describing an test plan template with all of its properties."""

    __test__ = False

    ID = "ID"
    NAME = "NAME"
    TEMPLATE_GROUP = "TEMPLATE_GROUP"
    PRODUCT_FAMILIES = "PRODUCT_FAMILIES"
    PART_NUMBERS = "PART_NUMBERS"
    SUMMARY = "SUMMARY"
    DESCRIPTION = "DESCRIPTION"
    TEST_PROGRAM = "TEST_PROGRAM"
    ESTIMATED_DURATION_IN_SECONDS = "ESTIMATED_DURATION_IN_SECONDS"
    SYSTEM_FILTER = "SYSTEM_FILTER"
    DUT_FILTER = "DUT_FILTER"
    EXECUTION_ACTIONS = "EXECUTION_ACTIONS"
    FILE_IDS = "FILE_IDS"
    WORKSPACE = "WORKSPACE"
    PROPERTIES = "PROPERTIES"
    DASHBOARD = "DASHBOARD"
    CREATED_BY = "CREATED_BY"
    UPDATED_BY = "UPDATED_BY"
    CREATED_AT = "CREATED_AT"
    UPDATED_AT = "UPDATED_AT"


class QueryTestPlanTemplatesRequest(WithPaging):
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
    `dutFilter`: String representing the LINQ filter used to filter the potential list of DUTs
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

    projection: Optional[List[TestPlanTemplateField]] = None
    """
    Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """
