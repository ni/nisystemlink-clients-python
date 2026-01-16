from enum import Enum
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class WorkItemTemplateField(str, Enum):
    """Enumeration of work item template fields that can be projected in query results."""

    ID = "ID"
    PRODUCT_FAMILIES = "PRODUCT_FAMILIES"
    PART_NUMBERS = "PART_NUMBERS"
    NAME = "NAME"
    SUMMARY = "SUMMARY"
    DESCRIPTION = "DESCRIPTION"
    TEMPLATE_GROUP = "TEMPLATE_GROUP"
    TEST_PROGRAM = "TEST_PROGRAM"
    TYPE = "TYPE"
    TIMELINE = "TIMELINE"
    TIMELINE_ESTIMATED_DURATION_IN_SECONDS = "TIMELINE_ESTIMATED_DURATION_IN_SECONDS"
    RESOURCES = "RESOURCES"
    RESOURCES_SYSTEMS = "RESOURCES_SYSTEMS"
    RESOURCES_ASSETS = "RESOURCES_ASSETS"
    RESOURCES_DUTS = "RESOURCES_DUTS"
    RESOURCES_FIXTURES = "RESOURCES_FIXTURES"
    RESOURCES_ASSETS_FILTER = "RESOURCES_ASSETS_FILTER"
    RESOURCES_DUTS_FILTER = "RESOURCES_DUTS_FILTER"
    RESOURCES_FIXTURES_FILTER = "RESOURCES_FIXTURES_FILTER"
    RESOURCES_SYSTEMS_FILTER = "RESOURCES_SYSTEMS_FILTER"
    WORKSPACE = "WORKSPACE"
    CREATED_BY = "CREATED_BY"
    UPDATED_BY = "UPDATED_BY"
    EXECUTION_ACTIONS = "EXECUTION_ACTIONS"
    FILE_IDS = "FILE_IDS"
    CREATED_AT = "CREATED_AT"
    UPDATED_AT = "UPDATED_AT"
    PROPERTIES = "PROPERTIES"
    DASHBOARD = "DASHBOARD"
    WORKFLOW_ID = "WORKFLOW_ID"


class WorkItemTemplateOrderBy(str, Enum):
    """Enumeration of fields by which work item templates can be ordered."""

    ID = "ID"
    NAME = "NAME"
    TEMPLATE_GROUP = "TEMPLATE_GROUP"
    CREATED_AT = "CREATED_AT"
    UPDATED_AT = "UPDATED_AT"


class QueryWorkItemTemplatesRequest(JsonModel):
    """Represents the request body content for querying work item templates.
    Allows filtering, sorting, and pagination of work item template results.
    """

    filter: str | None = None
    """A string expression to filter the work item templates returned by the query.

    `"@0"`, `"@1"` etc. can be used in conjunction with the `substitutions` parameter to keep this
    query string more simple and reusable.
    """

    substitutions: List[bool | int | str | None] | None = None
    """Makes substitutions in the query filter expression.

    Substitutions for the query expression are indicated by non-negative integers that are
    prefixed with the @ symbol. Each substitution in the given expression will be replaced by
    the element at the corresponding index (zero-based) in this list.
    """

    take: int | None = None
    """The maximum number of work item templates to return in the response."""

    order_by: WorkItemTemplateOrderBy | None = None
    """The field name to use for sorting the work item templates."""

    descending: bool | None = None
    """Whether to return the work item templates in descending order."""

    continuation_token: str | None = None
    """A token which allows the user to resume a query at the next item in the matching results.

    When querying, a token will be returned if a query may be continued. To obtain the next page
    of results, pass the token to the service on a subsequent request.
    """

    projection: List[WorkItemTemplateField] | None = None
    """
    Gets or sets the projection to be used when retrieving the work item templates. If not specified,
    all properties will be returned.
    """
