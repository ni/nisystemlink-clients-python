import enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._order_by import OrderBy


class TestPlanField(enum.Enum):
    """Model for an object describing an test plan with all of its properties."""

    ID = enum.auto()
    TEMPLATE_ID = enum.auto()
    NAME = enum.auto()
    STATE = enum.auto()
    SUBSTATE = enum.auto()
    DESCRIPTION = enum.auto()
    ASSIGNED_TO = enum.auto()
    WORK_ORDER_ID = enum.auto()
    WORK_ORDER_NAME = enum.auto()
    WORKSPACE = enum.auto()
    CREATED_BY = enum.auto()
    UPDATED_BY = enum.auto()
    CREATED_AT = enum.auto()
    UPDATED_AT = enum.auto()
    PROPERTIES = enum.auto()
    PART_NUMBER = enum.auto()
    DUT_ID = enum.auto()
    TEST_PROGRAM = enum.auto()
    SYSTEM_ID = enum.auto()
    FIXTURE_IDS = enum.auto()
    SYSTEM_FILTER = enum.auto()
    PLANNED_START_DATE_TIME = enum.auto()
    ESTIMATED_END_DATE_TIME = enum.auto()
    ESTIMATED_DURATION_IN_SECONDS = enum.auto()
    FILE_IDS_FROM_TEMPLATE = enum.auto()
    EXECUTION_ACTIONS = enum.auto()
    EXECUTION_HISTORY = enum.auto()
    DASHBOARD_URL = enum.auto()
    DASHBOARD = enum.auto()
    WORKFLOW = enum.auto()


class QueryTestPlansRequest(JsonModel):
    """Represents the request body for querying test plans.
    Allows filtering, sorting, and pagination of test plan results.
    """

    filter: Optional[str] = None
    """A string expression to filter the test plans returned by the query."""

    take: Optional[int] = None
    """The maximum number of test plans to return in the response."""

    order_by: Optional[OrderBy] = None
    """The field name to use for sorting the test plans."""

    descending: Optional[bool] = None
    """Whether to sort the test plans in descending order."""

    return_count: Optional[bool] = None
    """Whether to include the total count of matching test plans in the response."""

    continuation_token: Optional[str] = None
    """A token to retrieve the next page of results for paginated queries."""

    projection: Optional[List[TestPlanField]] = None
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

    projection: Optional[List[str]] = None
    """Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """
