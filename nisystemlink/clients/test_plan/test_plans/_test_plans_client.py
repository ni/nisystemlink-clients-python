from uplink import Field
from typing import Optional
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._methods import get, post
from nisystemlink.clients import core
from .models import (
    TestPlan,
    CreateTestPlansRequest,
    CreateTestPlansResponse,
    ScheduleTestPlansRequest,
    ScheduleTestPlansResponse,
    QueryTestPlansRequest,
    QueryTestPlansResponse,
    UpdateTestPlansRequest,
    UpdateTestPlansResponse,
    DeleteTestPlansResponse,
    DeleteTestPlansRequest
)

class TestPlansClient(BaseClient):
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

    @post("testplans", args=[Field("test_plan")])
    def create_test_plan(self, test_plan: CreateTestPlansRequest) -> CreateTestPlansResponse:
        """Create a new test plan.

        Args:
            test_plan: The test plan to create.

        Returns:
            The created test plan object.
        """
        ...

    @post("delete-testplans", args=[Field("test_plan_ids")])
    def delete_test_plans(self, test_plan_ids: DeleteTestPlansRequest) -> DeleteTestPlansResponse:
        """Delete test plans by IDs.

        Args:
            test_plan_ids: A list of test plan IDs to delete.

        Returns:
            None
        """
        ...

    @post("query-testplans", args=[Field("query")])
    def query_test_plans(self, query: QueryTestPlansRequest) -> QueryTestPlansResponse:
        """Query test plans.

        Args:
            query: The query to execute.

        Returns:
            A QueryTestPlansResponse object containing test plans that match the query.
        """
        ...

    @post("schedule-testplans", args=[Field("schedule")])
    def schedule_test_plan(self, schedule: ScheduleTestPlansRequest) -> ScheduleTestPlansResponse:
        """Schedule a test plan.

        Args:
            schedule: The schedule to apply to the test plan.

        Returns:
            A ScheduleTestPlansResponse object containing the scheduled test plan.
        """
        ...

    @post("update-testplans", args=[Field("test_plans")])
    def update_test_plan(self, test_plans: UpdateTestPlansRequest) -> UpdateTestPlansResponse:
        """Update a test plan.

        Args:
            test_plan: The test plan to update.

        Returns:
            The updated test plan object.
        """
        ...
