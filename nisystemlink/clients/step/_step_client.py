from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from uplink import Field, Query

from . import models


class StepClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Step Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/nitestmonitor/v2/")

    @post("steps")
    def create_steps(
        self, steps: models.CreateStepsRequest
    ) -> models.CreateStepsPartialSuccess:
        """Creates one or more steps.

        Args:
            steps: A list of steps to create.

        Returns:
            A list of steps that were successfully created and ones that failed to be created.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are
            invalid arguments.
        """
        ...

    @post("delete-steps", args=[Field("steps")])
    def delete_steps(
        self, steps: List[models.StepIdResultIdPair]
    ) -> Optional[models.DeleteStepsPartialSuccess]:
        """Deletes one or more steps by global id.

        Args:
            ids: a list of step ids. Note that these are the global ids and not the
            `stepId` that is local to a product and workspace.

        Returns:
            None if all deletes succeed otherwise a list of which ids failed and which succeeded.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are invalid
            arguments.
        """
        ...

    @post("query-steps")
    def query_steps(self, query: models.QueryStepsRequest) -> models.PagedSteps:
        """Queries for steps that match the filters.

        Args:
            query: The query contains a product id as well as a filter for steps under that product.

        Returns:
            A list of steps that match the filter.
        """
        ...

    @post("update-steps")
    def update_steps(
        self, steps: models.UpdateStepsRequest
    ) -> Optional[models.UpdateStepsPartialSuccess]:
        """Updates one or more steps.

        Update requires that the version field matches the version being updated from.

        Args:
            steps: a list of steps that are to be updated. Must include the global id and
            each step being updated must match the version currently on the server.

        Returns
            A list of steps that were successfully updated and a list of ones that were not along
            with error messages for updates that failed.
        """
        ...

    @get(
        "steps",
        args=[Query("continuationToken"), Query("take"), Query("returnCount")],
    )
    def get_steps_paged(
        self,
        continuation_token: Optional[str] = None,
        take: Optional[int] = None,
        return_count: Optional[bool] = None,
    ) -> models.PagedSteps:
        """Reads a list of steps.

        Args:
            continuation_token: The token used to paginate steps.
            take: The number of steps to get in this request.
            return_count: Whether or not to return the total number of steps available.

        Returns:
            A list of steps.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` Service
                or provided an invalid argument.
        """
        ...

    @get("results/{resultId}/steps/{stepId}")
    def get_step(self, result_id: str, step_id: str) -> models.Step:
        """Gets a single step.

        Args:
            result_id: The resultId of the step to get.
            step_id: The stepId of the step to get.

        Returns:
            The step.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` Service
                or provided an invalid argument.
        """
        ...

    @delete("results/{resultId}/steps/{stepId}", args=[Query("updateResultTotalTime")])
    def delete_step(
        self,
        result_id: str,
        step_id: str,
        update_result_total_time: Optional[bool] = False,
    ) -> None:
        """Deletes a single step.

        Args:
            result_id: The resultId of the step to delete.
            step_id: The stepId of the step to delete.
            update_result_total_time: Determine test result total time from the step total times.
                Defaults to False.

        Returns:
            None
        """
        ...

    @post("query-step-values")
    def query_step_values(self, query: models.QueryStepValuesRequest) -> List[str]:
        """Queries values for a step field.

        Args:
            query: The query parameters.

        Returns:
            A list of values for the specified step field.
        """
        ...
