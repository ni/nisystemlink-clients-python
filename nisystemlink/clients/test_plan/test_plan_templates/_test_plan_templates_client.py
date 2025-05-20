"""Implementation of Test plan template Client"""

from typing import List, Optional

from nisystemlink.clients import core
from uplink import Field, retry

from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import post

from . import models


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class TestPlanTemplateClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the `/niworkorder` Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()
        super().__init__(configuration, base_path="/niworkorder/v1/")

    @post("testplan-templates", args=[Field("testPlanTemplates")])
    def create_test_plan_templates(
        self, test_plan_templates: List[models.TestPlanTemplateBase]
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
    ) -> models.QueryTestPlanTemplatesResponse:
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
