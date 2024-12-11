from typing import List, Optional, Union, Any
import json

from nisystemlink.clients import core
from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post, response_handler
from uplink import Query
from requests.models import Response

from . import models


def _cancel_job_response_handler(response: Response) -> Union[ApiError, None]:
    """Response handler for Cancel Job response."""
    if response is None:
        return None

    try:
        cancel_response = response.json()
    except json.JSONDecodeError:
        return None

    return cancel_response.get("error")


def _list_jobs_response_handler(response: Response) -> List[models.Job]:
    """Response handler for List Jobs response."""
    if response is None:
        return []

    jobs = response.json()

    return jobs


class SystemClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the ``/nisysmgmt`` Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, "/nisysmgmt/v1/")

    @response_handler(_list_jobs_response_handler)
    @get(
        "jobs",
        args=[
            Query("systemId"),
            Query("jid"),
            Query("state"),
            Query("function"),
            Query("skip"),
            Query("take"),
        ],
    )
    def list_jobs(
        self,
        system_id: Optional[str] = None,
        job_id: Optional[str] = None,
        state: Optional[models.JobState] = None,
        function: Optional[str] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> List[models.Job]:
        """List the jobs that matched the criteria.

        Args:
            system_id: The ID of the system to that the jobs belong.
            jid: The ID of the job.
            state: The state of the jobs.
            function: The salt function to run on the client.
            skip: The number of jobs to skip.
            take: The number of jobs to return.

        Returns:
            The list of jobs that matched the criteria.

        Raises:
            ApiException: if unable to communicate with the ``/nisysmgmt`` Service
                or provided an invalid argument.
        """
        ...

    @post("jobs")
    def create_job(self, job: models.CreateJobRequest) -> models.CreateJobResponse:
        """Create a job.

        Args:
            job: The request to create the job.

        Returns:
            The job that was created.

        Raises:
            ApiException: if unable to communicate with the ``/nisysmgmt`` Service
                or provided an invalid argument.
        """
        ...

    @get("get-jobs-summary")
    def get_job_summary(self) -> models.JobSummaryResponse:
        """Get a summary of the jobs.

        Returns:
            An instance of a JobsSummaryResponse.

        Raises:
            ApiException: if unable to communicate with the ``/nisysmgmt`` Service
                or provided an invalid argument.
        """
        ...

    @post("query-jobs")
    def _query_jobs(self, query: models._QueryJobsRequest) -> models.QueryJobsResponse:
        """Query the jobs.

        Args:
            query: The request to query the jobs.

        Returns:
            An instance of QueryJobsRequest.

        Raises:
            ApiException: if unable to communicate with the ``/nisysmgmt`` Service
                or provided an invalid argument.
        """
        ...

    def query_jobs(self, query: models.QueryJobsRequest) -> models.QueryJobsResponse:
        """Query the jobs.

        Args:
            query: The request to query the jobs.

        Returns:
            An instance of QueryJobsRequest.

        Raises:
            ApiException: if unable to communicate with the ``/nisysmgmt`` Service
                or provided an invalid argument.
        """

        projection = ",".join(query.projection)
        projection = f"new({projection})" if projection else ""

        order_by = (
            f"{query.order_by.strip()} {'descending' if query.descending else 'ascending'}"
            if query.order_by
            else None
        )

        query_request = models._QueryJobsRequest(
            skip=query.skip,
            take=query.take,
            filter=query.filter,
            projection=projection,
            order_by=order_by,
        ).dict()

        # Remove None values from the dictionary
        query_params = {k: v for k, v in query_request.items() if v is not None}

        query_request = models._QueryJobsRequest(**query_params)

        print(query_request)

        return self._query_jobs(query_request)

    @response_handler(_cancel_job_response_handler)
    @post("cancel-jobs")
    def cancel_jobs(
        self, job_ids: List[models.CancelJobRequest]
    ) -> Union[ApiError, None]:
        """Cancel the jobs.

        Args:
            job_ids: List of CancelJobRequest.

        Returns:
            The errors that appear while attempting the operation.

        Raises:
            ApiException: if unable to communicate with the ``/nisysmgmt`` Service
                or provided an invalid argument.
        """
        ...
