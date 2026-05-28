import warnings
from typing import List

from nisystemlink.clients import core
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
from nisystemlink.clients.test_plan import models
from uplink import Field, retry

from ..core.helpers._partial_success import unwrap_single_item_partial_success


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class TestPlanClient(BaseClient):
    __test__ = False

    def __init__(self, configuration: HttpConfiguration | None = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the WorkOrder Service.
        """
        warnings.warn(
            "TestPlanClient is deprecated and will be removed in the future. "
            "Use WorkItemClient instead.",
            DeprecationWarning,
            stacklevel=2,
        )
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

    def create_test_plan(
        self, test_plan: models.CreateTestPlanRequest
    ) -> models.TestPlan:
        """Create a single test plan.

        Args:
            test_plan: The test plan to create.

        Returns:
            The created test plan.

        Raises:
            ApiException: if the test plan could not be created or the service returns an
                unexpected partial-success payload.
        """
        response = self.create_test_plans([test_plan])

        return unwrap_single_item_partial_success(
            response=response,
            items=response.created_test_plans,
            failed=response.failed_test_plans,
            error=response.error,
            failure_message="Failed to create test plan.",
            empty_message="Server returned no created test plans.",
        )

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

    def schedule_test_plan(
        self,
        test_plan: models.ScheduleTestPlanRequest,
        replace: bool | None = None,
    ) -> models.TestPlan:
        """Schedule a single test plan.

        Args:
            test_plan: The test plan schedule request.
            replace: Whether to replace the existing scheduled test plan.

        Returns:
            The scheduled test plan.

        Raises:
            ApiException: if the test plan could not be scheduled or the service returns an
                unexpected partial-success payload.
        """
        response = self.schedule_test_plans(
            models.ScheduleTestPlansRequest(test_plans=[test_plan], replace=replace)
        )

        return unwrap_single_item_partial_success(
            response=response,
            items=response.scheduled_test_plans,
            failed=response.failed_test_plans,
            error=response.error,
            failure_message="Failed to schedule test plan.",
            empty_message="Server returned no scheduled test plans.",
        )

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

    def update_test_plan(
        self, test_plan: models.UpdateTestPlanRequest, replace: bool | None = None
    ) -> models.TestPlan:
        """Update a single test plan.

        Args:
            test_plan: The test plan to update.
            replace: Whether to replace the existing test plan instead of merging updates.

        Returns:
            The updated test plan.

        Raises:
            ApiException: if the test plan could not be updated or the service returns an
                unexpected partial-success payload.
        """
        response = self.update_test_plans(
            models.UpdateTestPlansRequest(test_plans=[test_plan], replace=replace)
        )

        return unwrap_single_item_partial_success(
            response=response,
            items=response.updated_test_plans,
            failed=response.failed_test_plans,
            error=response.error,
            failure_message="Failed to update test plan.",
            empty_message="Server returned no updated test plans.",
        )

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

    def create_test_plan_template(
        self, test_plan_template: models.CreateTestPlanTemplateRequest
    ) -> models.TestPlanTemplate:
        """Creates a single test plan template.

        Args:
            test_plan_template: The test plan template to create.

        Returns:
            The created test plan template.

        Raises:
            ApiException: if the test plan template could not be created or the service returns an
                unexpected partial-success payload.
        """
        response = self.create_test_plan_templates([test_plan_template])

        return unwrap_single_item_partial_success(
            response=response,
            items=response.created_test_plan_templates,
            failed=response.failed_test_plan_templates,
            error=response.error,
            failure_message="Failed to create test plan template.",
            empty_message="Server returned no created test plan templates.",
        )

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
    ) -> models.DeleteTestPlanTemplatesPartialSuccessResponse | None:
        """Deletes one or more test plan templates and return errors for failed deletion.

        Returns:
            A partial success if any test plan templates failed to delete, or None if all
            test plan templates were deleted successfully.

        Raises: ApiException: if unable to communicate with the `/niworkorder` service of provided invalid
            arguments.
        """
        ...
