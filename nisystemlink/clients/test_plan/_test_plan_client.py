from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
from nisystemlink.clients.test_plan import models
from uplink import Field, retry


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class TestPlanClient(BaseClient):
    __test__ = False

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
    def get_test_plan(self, test_plan_id: str) -> models.TestPlan:
        """Retrieve a test plan by its ID.

        Args:
            test_plan_id: The ID of the test plan to retrieve.

        Returns:
            The TestPlan object corresponding to the given ID.
        """
        ...

    @post("testplans", args=[Field("testPlans")])
    def create_test_plans(
        self, test_plans: List[models.CreateTestPlanRequest]
    ) -> models.CreateTestPlansPartialSuccessResponse:
        """Create a new test plan.

        Args:
            test_plan: The test plans to create.

        Returns:
            The created test plan object.
        """
        ...

    @post("delete-testplans", args=[Field("ids")])
    def delete_test_plans(self, ids: List[str]) -> None:
        """Delete test plans by IDs.

        Args:
            test_plan_ids: A list of test plan IDs to delete.

        Returns:
            None
        """
        ...

    @post("query-testplans")
    def query_test_plans(
        self, query_request: models.QueryTestPlansRequest
    ) -> models.PagedTestPlans:
        """Query test plans.

        Args:
            query: The query to execute.

        Returns:
            A PagedTestPlans object containing test plans that match the query.
        """
        ...

    @post("schedule-testplans")
    def schedule_test_plans(
        self, schedule_request: models.ScheduleTestPlansRequest
    ) -> models.ScheduleTestPlansResponse:
        """Schedule a test plan.

        Args:
            schedule: The schedule to apply to the test plan.

        Returns:
            A ScheduleTestPlansResponse object containing the scheduled test plan.
        """
        ...

    @post("update-testplans")
    def update_test_plans(
        self, update_request: models.UpdateTestPlansRequest
    ) -> models.UpdateTestPlansResponse:
        """Update a test plan.

        Args:
            test_plan: The test plan to update.

        Returns:
            The updated test plan object.
        """
        ...

    @post("testplan-templates", args=[Field("testPlanTemplates")])
    def create_test_plan_templates(
        self, test_plan_templates: List[models.CreateTestPlanTemplateRequest]
    ) -> models.CreateTestPlanTemplatePartialSuccessResponse:
        """Creates one or more test plan template and return errors for failed creations.

        Args:
            test_plan_templates: A list of test plan templates to attempt to create.

        Returns: A list of created test plan templates, test plan templates that failed to create, and errors for
                 failures.

        Raises: ApiException: if unable to communicate with the `/niworkorder` service of provided invalid
                arguments.
        """
        ...

    @post("query-testplan-templates")
    def query_test_plan_templates(
        self, query_test_plan_templates: models.QueryTestPlanTemplatesRequest
    ) -> models.PagedTestPlanTemplates:
        """Queries one or more test plan templates and return errors for failed queries.

        Returns: A list of test plan templates, based on the query and errors for the wrong query.

        Raises: ApiException: if unable to communicate with the `/niworkorder` service of provided invalid
                arguments.
        """
        ...

    @post("delete-testplan-templates", args=[Field("ids")])
    def delete_test_plan_templates(
        self, ids: List[str]
    ) -> Optional[models.DeleteTestPlanTemplatesPartialSuccessResponse]:
        """Deletes one or more test plan templates and return errors for failed deletion.

        Returns:
            A partial success if any test plan templates failed to delete, or None if all
            test plan templates were deleted successfully.

        Raises: ApiException: if unable to communicate with the `/niworkorder` service of provided invalid
            arguments.
        """
        ...
