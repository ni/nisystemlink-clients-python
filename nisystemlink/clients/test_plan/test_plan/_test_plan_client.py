from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
from nisystemlink.clients.test_plan.test_plan.models._paged_test_plans import (
    PagedTestPlans,
)
from uplink import retry


from .models import (
    _QueryTestPlansRequest,
    CreateTestPlansRequest,
    CreateTestPlansResponse,
    DeleteTestPlansRequest,
    QueryTestPlansRequest,
    ScheduleTestPlansRequest,
    ScheduleTestPlansResponse,
    TestPlan,
    UpdateTestPlansRequest,
    UpdateTestPlansResponse,
)


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class TestPlanClient(BaseClient):
    def __init__(self, configuration: Optional[HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the WorkOrder Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/niworkorder/v1/")

    @get("testplans/{test_plan_id}")
    def get_test_plan(self, test_plan_id) -> TestPlan:
        """Retrieve a test plan by its ID.

        Args:
            test_plan_id: The ID of the test plan to retrieve.

        Returns:
            The TestPlan object corresponding to the given ID.
        """
        ...

    @post("testplans")
    def create_test_plans(
        self, create_request: CreateTestPlansRequest
    ) -> CreateTestPlansResponse:
        """Create a new test plan.

        Args:
            test_plan: The test plans to create.

        Returns:
            The created test plan object.
        """
        ...

    @post("delete-testplans")
    def delete_test_plans(self, ids: DeleteTestPlansRequest) -> None:
        """Delete test plans by IDs.

        Args:
            test_plan_ids: A list of test plan IDs to delete.

        Returns:
            None
        """
        ...

    @post("query-testplans")
    def __query_test_plans(
        self, query_request: _QueryTestPlansRequest
    ) -> PagedTestPlans:
        """Query test plans.

        Args:
            query: The query to execute.

        Returns:
            A PagedTestPlans object containing test plans that match the query.
        """
        ...

    def query_test_plans(self, query_request: QueryTestPlansRequest) -> PagedTestPlans:
        """Query test plans.

        Args:
            query: The query to execute.

        Returns:
            A PagedTestPlans object containing test plans that match the query.
        """
        projection_str = (
            [projection.name for projection in query_request.projection]
            if query_request.projection
            else None
        )
        query_params = {
            "filter": query_request.filter,
            "take": query_request.take,
            "continuation_token": query_request.continuation_token,
            "order_by": query_request.order_by,
            "descending": query_request.descending,
            "return_count": query_request.return_count,
            "projection": projection_str,
        }

        query_params = {k: v for k, v in query_params.items() if v is not None}

        query_test_plans_request = _QueryTestPlansRequest(**query_params)

        return self.__query_test_plans(query_request=query_test_plans_request)

    @post("schedule-testplans")
    def schedule_test_plans(
        self, schedule_request: ScheduleTestPlansRequest
    ) -> ScheduleTestPlansResponse:
        """Schedule a test plan.

        Args:
            schedule: The schedule to apply to the test plan.

        Returns:
            A ScheduleTestPlansResponse object containing the scheduled test plan.
        """
        ...

    @post("update-testplans")
    def update_test_plans(
        self, update_request: UpdateTestPlansRequest
    ) -> UpdateTestPlansResponse:
        """Update a test plan.

        Args:
            test_plan: The test plan to update.

        Returns:
            The updated test plan object.
        """
        ...
