from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class TestPlanField(str, Enum):
    """Model for an object describing an test plan with all of its properties."""

    ID = "id"
    TEMPLATE_ID = "templateId"
    NAME = "name"
    STATE = "state"
    SUBSTATE = "substate"
    DESCRIPTION = "description"
    ASSIGNED_TO = "assignedTo"
    WORK_ORDER_ID = "workOrderId"
    WORK_ORDER_NAME = "workOrderName"
    WORKSPACE = "workspace"
    CREATED_BY = "createdBy"
    UPDATED_BY = "updatedBy"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    PROPERTIES = "properties"
    PART_NUMBER = "partNumber"
    DUT_ID = "dutId"
    TEST_PROGRAM = "testProgram"
    SYSTEM_ID = "systemId"
    FIXTURE_IDS = "fixtureIds"
    SYSTEM_FILTER = "systemFilter"
    PLANNED_START_DATE_TIME = "plannedStartDateTime"
    ESTIMATED_END_DATE_TIME = "estimatedEndDateTime"
    ESTIMATED_DURATION_IN_SECONDS = "estimatedDurationInSeconds"
    FILE_IDS_FROM_TEMPLATE = "fileIdsFromTemplate"
    EXECUTION_ACTIONS = "executionActions"
    EXECUTION_HISTORY = "executionHistory"
    DASHBOARD_URL = "dashboardUrl"
    DASHBOARD = "dashboard"
    WORKFLOW = "workflow"


class QueryTestPlansRequest(JsonModel):
    """Represents the request body for querying test plans.
    Allows filtering, sorting, and pagination of test plan results.
    """

    filter: Optional[str] = None
    """A string expression to filter the test plans returned by the query."""

    take: Optional[int] = None
    """The maximum number of test plans to return in the response."""

    order_by: Optional[str] = None
    """The field name to use for sorting the test plans."""

    descending: Optional[bool] = None
    """Whether to sort the test plans in descending order."""

    return_count: Optional[bool] = None
    """Whether to include the total count of matching test plans in the response."""

    continuation_token: Optional[str] = None
    """A token to retrieve the next page of results for paginated queries."""

    projection: List[TestPlanField] = []
    """
    Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """


class _QueryTestPlansRequest(JsonModel):
    """Represents the request body for querying test plans.
    Allows filtering, sorting, and pagination of test plan results.
    """

    filter: Optional[str] = None
    """A string expression to filter the test plans returned by the query."""

    take: Optional[int] = None
    """The maximum number of test plans to return in the response."""

    order_by: Optional[str] = None
    """The field name to use for sorting the test plans."""

    descending: Optional[bool] = None
    """Whether to sort the test plans in descending order."""

    return_count: Optional[bool] = None
    """Whether to include the total count of matching test plans in the response."""

    continuation_token: Optional[str] = None
    """A token to retrieve the next page of results for paginated queries."""

    projection: Optional[str] = None
    """Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """
