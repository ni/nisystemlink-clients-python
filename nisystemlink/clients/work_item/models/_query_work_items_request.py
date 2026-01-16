from enum import Enum
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class WorkItemField(str, Enum):
    """Enumeration of work item fields that can be projected in query results."""

    ID = "ID"
    NAME = "NAME"
    TYPE = "TYPE"
    STATE = "STATE"
    SUBSTATE = "SUBSTATE"
    DESCRIPTION = "DESCRIPTION"
    PARENT_ID = "PARENT_ID"
    TEMPLATE_ID = "TEMPLATE_ID"
    ASSIGNED_TO = "ASSIGNED_TO"
    REQUESTED_BY = "REQUESTED_BY"
    TEST_PROGRAM = "TEST_PROGRAM"
    PART_NUMBER = "PART_NUMBER"
    TIMELINE = "TIMELINE"
    TIMELINE_EARLIEST_START_DATE_TIME = "TIMELINE_EARLIEST_START_DATE_TIME"
    TIMELINE_DUE_DATE_TIME = "TIMELINE_DUE_DATE_TIME"
    TIMELINE_ESTIMATED_DURATION_IN_SECONDS = "TIMELINE_ESTIMATED_DURATION_IN_SECONDS"
    SCHEDULE = "SCHEDULE"
    SCHEDULE_PLANNED_START_DATE_TIME = "SCHEDULE_PLANNED_START_DATE_TIME"
    SCHEDULE_PLANNED_END_DATE_TIME = "SCHEDULE_PLANNED_END_DATE_TIME"
    SCHEDULE_PLANNED_DURATION_IN_SECONDS = "SCHEDULE_PLANNED_DURATION_IN_SECONDS"
    RESOURCES = "RESOURCES"
    RESOURCES_SYSTEMS = "RESOURCES_SYSTEMS"
    RESOURCES_ASSETS = "RESOURCES_ASSETS"
    RESOURCES_DUTS = "RESOURCES_DUTS"
    RESOURCES_FIXTURES = "RESOURCES_FIXTURES"
    RESOURCES_SYSTEMS_SELECTIONS = "RESOURCES_SYSTEMS_SELECTIONS"
    RESOURCES_SYSTEMS_SELECTIONS_ID = "RESOURCES_SYSTEMS_SELECTIONS_ID"
    RESOURCES_SYSTEMS_SELECTIONS_TARGET_LOCATION_ID = (
        "RESOURCES_SYSTEMS_SELECTIONS_TARGET_LOCATION_ID"
    )
    RESOURCES_ASSETS_SELECTIONS = "RESOURCES_ASSETS_SELECTIONS"
    RESOURCES_ASSETS_SELECTIONS_ID = "RESOURCES_ASSETS_SELECTIONS_ID"
    RESOURCES_ASSETS_SELECTIONS_TARGET_LOCATION_ID = (
        "RESOURCES_ASSETS_SELECTIONS_TARGET_LOCATION_ID"
    )
    RESOURCES_ASSETS_SELECTIONS_TARGET_SYSTEM_ID = (
        "RESOURCES_ASSETS_SELECTIONS_TARGET_SYSTEM_ID"
    )
    RESOURCES_ASSETS_SELECTIONS_TARGET_PARENT_ID = (
        "RESOURCES_ASSETS_SELECTIONS_TARGET_PARENT_ID"
    )
    RESOURCES_DUTS_SELECTIONS = "RESOURCES_DUTS_SELECTIONS"
    RESOURCES_DUTS_SELECTIONS_ID = "RESOURCES_DUTS_SELECTIONS_ID"
    RESOURCES_DUTS_SELECTIONS_TARGET_LOCATION_ID = (
        "RESOURCES_DUTS_SELECTIONS_TARGET_LOCATION_ID"
    )
    RESOURCES_DUTS_SELECTIONS_TARGET_PARENT_ID = (
        "RESOURCES_DUTS_SELECTIONS_TARGET_PARENT_ID"
    )
    RESOURCES_DUTS_SELECTIONS_TARGET_SYSTEM_ID = (
        "RESOURCES_DUTS_SELECTIONS_TARGET_SYSTEM_ID"
    )
    RESOURCES_FIXTURES_SELECTIONS = "RESOURCES_FIXTURES_SELECTIONS"
    RESOURCES_FIXTURES_SELECTIONS_ID = "RESOURCES_FIXTURES_SELECTIONS_ID"
    RESOURCES_FIXTURES_SELECTIONS_TARGET_LOCATION_ID = (
        "RESOURCES_FIXTURES_SELECTIONS_TARGET_LOCATION_ID"
    )
    RESOURCES_FIXTURES_SELECTIONS_TARGET_PARENT_ID = (
        "RESOURCES_FIXTURES_SELECTIONS_TARGET_PARENT_ID"
    )
    RESOURCES_FIXTURES_SELECTIONS_TARGET_SYSTEM_ID = (
        "RESOURCES_FIXTURES_SELECTIONS_TARGET_SYSTEM_ID"
    )
    RESOURCES_ASSETS_FILTER = "RESOURCES_ASSETS_FILTER"
    RESOURCES_DUTS_FILTER = "RESOURCES_DUTS_FILTER"
    RESOURCES_FIXTURES_FILTER = "RESOURCES_FIXTURES_FILTER"
    RESOURCES_SYSTEMS_FILTER = "RESOURCES_SYSTEMS_FILTER"
    FILE_IDS_FROM_TEMPLATE = "FILE_IDS_FROM_TEMPLATE"
    PROPERTIES = "PROPERTIES"
    DASHBOARD = "DASHBOARD"
    CREATED_BY = "CREATED_BY"
    CREATED_AT = "CREATED_AT"
    UPDATED_BY = "UPDATED_BY"
    UPDATED_AT = "UPDATED_AT"
    WORKSPACE = "WORKSPACE"
    WORKFLOW_ID = "WORKFLOW_ID"


class WorkItemOrderBy(str, Enum):
    """Enumeration of fields by which work items can be ordered."""

    ID = "ID"
    UPDATED_AT = "UPDATED_AT"


class QueryWorkItemsRequest(JsonModel):
    """Represents the request body content for querying work items.
    Allows filtering, sorting, and pagination of work item results.
    """

    filter: str | None = None
    """A string expression to filter the work items returned by the query.

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
    """The maximum number of work items to return in the response."""

    continuation_token: str | None = None
    """A token which allows the user to resume a query at the next item in the matching results.

    When querying, a token will be returned if a query may be continued. To obtain the next page
    of results, pass the token to the service on a subsequent request.
    """

    order_by: WorkItemOrderBy | None = None
    """The field name to use for sorting the work items."""

    descending: bool | None = None
    """Whether to sort the work items in descending order."""

    return_count: bool | None = None
    """Whether to include the total count of matching work items in the response."""

    projection: List[WorkItemField] | None = None
    """
    Gets or sets the projection to be used when retrieving the work items. If not specified,
    all properties will be returned.
    """
