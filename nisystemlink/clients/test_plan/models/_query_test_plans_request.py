import enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._order_by import OrderBy


class TestPlanField(enum.Enum):
    """Model for an object describing an test plan with all of its properties."""

    __test__ = False

    ID = "ID"
    TEMPLATE_ID = "TEMPLATE_ID"
    NAME = "NAME"
    STATE = "STATE"
    SUBSTATE = "SUBSTATE"
    DESCRIPTION = "DESCRIPTION"
    ASSIGNED_TO = "ASSIGNED_TO"
    WORK_ORDER_ID = "WORK_ORDER_ID"
    WORK_ORDER_NAME = "WORK_ORDER_NAME"
    PART_NUMBER = "PART_NUMBER"
    DUT_ID = "DUT_ID"
    DUT_SERIAL_NUMBER = "DUT_SERIAL_NUMBER"
    TEST_PROGRAM = "TEST_PROGRAM"
    WORKSPACE = "WORKSPACE"
    CREATED_BY = "CREATED_BY"
    UPDATED_BY = "UPDATED_BY"
    SYSTEM_ID = "SYSTEM_ID"
    FIXTURE_IDS = "FIXTURE_IDS"
    PLANNED_START_DATE_TIME = "PLANNED_START_DATE_TIME"
    ESTIMATED_END_DATE_TIME = "ESTIMATED_END_DATE_TIME"
    ESTIMATED_DURATION_IN_SECONDS = "ESTIMATED_DURATION_IN_SECONDS"
    SYSTEM_FILTER = "SYSTEM_FILTER"
    DUT_FILTER = "DUT_FILTER"
    CREATED_AT = "CREATED_AT"
    UPDATED_AT = "UPDATED_AT"
    PROPERTIES = "PROPERTIES"
    FILE_IDS_FROM_TEMPLATE = "FILE_IDS_FROM_TEMPLATE"
    DASHBOARD = "DASHBOARD"
    EXECUTION_ACTIONS = "EXECUTION_ACTIONS"
    EXECUTION_HISTORY = "EXECUTION_HISTORY"
    DASHBOARD_URL = "DASHBOARD_URL"
    WORKFLOW = "WORKFLOW"


class QueryTestPlansRequest(WithPaging):
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

    projection: Optional[List[TestPlanField]] = None
    """
    Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """
