"""Implementation of TestMonitor Client"""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from nisystemlink.clients.testmonitor.models import (
    CreateResultRequest,
    UpdateResultRequest,
)
from uplink import Field, Path, Query, retry, returns

from . import models


@retry(
    when=retry.when.status([408, 429, 502, 503, 504]), stop=retry.stop.after_attempt(5)
)
class TestMonitorClient(BaseClient):
    # prevent pytest from thinking this is a test class
    __test__ = False

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the TestMonitor Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()
        super().__init__(configuration, base_path="/nitestmonitor/v2/")

    @get("")
    def api_info(self) -> models.ApiInfo:
        """Get information about the available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the `ni``/nitestmonitor``` service.
        """
        ...

    @post("results", args=[Field("results")])
    def create_results(
        self, results: List[CreateResultRequest]
    ) -> models.CreateResultsPartialSuccess:
        """Creates one or more results and returns errors for failed creations.

        Args:
            results: A list of results to attempt to create.

        Returns: A list of created results, results that failed to create, and errors for
            failures.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` service of provided invalid
                arguments.
        """
        ...

    @get(
        "results",
        args=[Query("continuationToken"), Query("take"), Query("returnCount")],
    )
    def get_results(
        self,
        continuation_token: Optional[str] = None,
        take: Optional[int] = None,
        return_count: Optional[bool] = None,
    ) -> models.PagedResults:
        """Reads a list of results.

        Args:
            continuation_token: The token used to paginate results.
            take: The number of results to get in this request.
            return_count: Whether or not to return the total number of results available.

        Returns:
            A list of results.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @get("results/{id}")
    def get_result(self, id: str) -> models.Result:
        """Retrieves a single result by id.

        Args:
            id (str): Unique ID of a result.

        Returns:
            The single result matching `id`

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @post("query-results")
    def query_results(self, query: models.QueryResultsRequest) -> models.PagedResults:
        """Queries for results that match the filter.

        Args:
            query : The query contains a DynamicLINQ query string in addition to other details
                about how to filter and return the list of results.

        Returns:
            A paged list of results with a continuation token to get the next page.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service or provided invalid
                arguments.
        """
        ...

    @returns.json  # type: ignore
    @post("query-result-values")
    def query_result_values(self, query: models.QueryResultValuesRequest) -> List[str]:
        """Queries for results that match the query and returns a list of the requested field.

        Args:
            query : The query for the fields.

        Returns:
            A list of the values of the queried field.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service or provided
                invalid arguments.
        """
        ...

    @post("update-results", args=[Field("results"), Field("replace")])
    def update_results(
        self, results: List[UpdateResultRequest], replace: bool = False
    ) -> models.UpdateResultsPartialSuccess:
        """Updates a list of results with optional field replacement.

        Args:
            `results`: A list of results to update. Results are matched for update by id.
            `replace`: Replace the existing fields instead of merging them. Defaults to `False`.
                If this is `True`, then `keywords` and `properties` for the result will be
                    replaced by what is in the `results` provided in this request.
                If this is `False`, then the `keywords` and `properties` in this request will
                    merge with what is already present in the server resource.

        Returns: A list of updates results, results that failed to update, and errors for
            failures.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @delete("results/{id}")
    def delete_result(self, id: str) -> None:
        """Deletes a single result by id.

        Args:
            id (str): Unique ID of a result.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @post("delete-results", args=[Field("ids")])
    def delete_results(
        self, ids: List[str]
    ) -> Optional[models.DeleteResultsPartialSuccess]:
        """Deletes multiple results.

        Args:
            ids (List[str]): List of unique IDs of results.

        Returns:
            A partial success if any results failed to delete, or None if all
            results were deleted successfully.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @post(
        "steps",
        args=[Field("steps"), Field("updateResultTotalTime")],
    )
    def create_steps(
        self,
        steps: List[models.CreateStepRequest],
        update_result_total_time: bool = False,
    ) -> models.CreateStepsPartialSuccess:
        """Creates one or more steps.

        Args:
            steps: A list of steps to create.
            update_result_total_time: Determine test result total time from the step total times.
                Defaults to False.

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
        """Deletes one or more steps by global ID.

        Args:
            steps: A list of step IDs and result IDs. Note that these are the global IDs and not the
            `step_id` that is local to a product and workspace.

        Returns:
            None if all deletes succeed otherwise a list of which IDs failed and which succeeded.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there
            invalid arguments.
        """
        ...

    @delete(
        "results/{resultId}/steps/{stepId}",
        args=[Path("resultId"), Path("stepId"), Query("updateResultTotalTime")],
    )
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

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are
            invalid arguments.
        """
        ...

    @post("query-steps")
    def query_steps(self, query: models.QueryStepsRequest) -> models.PagedSteps:
        """Queries for steps that match the filters.

        Args:
            query: The query contains a product ID as well as a filter for steps under that product.

        Returns:
            A list of steps that match the filter.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are
            invalid arguments.
        """
        ...

    @post(
        "update-steps",
        args=[
            Field("steps"),
            Field("updateResultTotalTime"),
            Field("replaceKeywords"),
            Field("replaceProperties"),
        ],
    )
    def update_steps(
        self,
        steps: List[models.UpdateStepRequest],
        update_result_total_time: bool = False,
        replace_keywords: bool = False,
        replace_properties: bool = False,
    ) -> models.UpdateStepsPartialSuccess:
        """Updates one or more steps.

        Update requires that the version field matches the version being updated from.

        Args:
            steps: a list of steps that are to be updated. Must include the global ID and
            each step being updated must match the version currently on the server.
            update_result_total_time: Determine test result total time from the step total times.
                Defaults to False.
            replace_keywords: Replace with existing keywords instead of merging them.
                Defaults to False.
            replace_properties: Replace with existing properties instead of merging them.
                Defaults to False.

        Returns
            A list of steps that were successfully updated and a list of ones that were not along
            with error messages for updates that failed.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are
            invalid arguments.
        """
        ...

    @get(
        "steps",
        args=[Query("continuationToken"), Query("take"), Query("returnCount")],
    )
    def get_steps(
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
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are
            invalid arguments..
        """
        ...

    @get("results/{resultId}/steps/{stepId}", args=[Path("resultId"), Path("stepId")])
    def get_step(self, result_id: str, step_id: str) -> models.Step:
        """Gets a single step.

        Args:
            result_id: The resultId of the step to get.
            step_id: The stepId of the step to get.

        Returns:
            The step.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are
            invalid arguments.
        """
        ...

    @returns.json  # type: ignore
    @post("query-step-values")
    def query_step_values(self, query: models.QueryStepValuesRequest) -> List[str]:
        """Queries values for a step field.

        Args:
            query: The query parameters.

        Returns:
            A list of values for the specified step field.

        Raises:
            ApiException: if unable to communicate with the `/nitestmonitor` service or if there are
            invalid arguments.
        """
        ...
