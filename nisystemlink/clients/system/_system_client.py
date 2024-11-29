from typing import Optional, List
from uplink import Query

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import (
    get,
    post,
)

from . import models


class SystemClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the System Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, "/nisysmgmt/v1/")

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
        jid: Optional[str] = None,
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
            ApiException: if unable to communicate with the System Service
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
            ApiException: if unable to communicate with the System Service
                or provided an invalid argument.
        """
        ...

    @get("get-jobs-summary")
    def get_job_summary(self) -> models.JobSummaryResponse:
        """Get a summary of the jobs.

        Returns:
            An instance of a JobsSummaryResponse.

        Raises:
            ApiException: if unable to communicate with the System Service
                or provided an invalid argument.
        """
        ...

    @post("query-jobs")
    def query_jobs(self, query: models.QueryJobsRequest) -> models.QueryJobsResponse:
        """Query the jobs.

        Args:
            query: The request to query the jobs.

        Returns:
            An instance of QueryJobsRequest.

        Raises:
            ApiException: if unable to communicate with the System Service
                or provided an invalid argument.
        """
        ...

    @post("cancel-jobs")
    def cancel_jobs(
        self, job_ids: List[models.CancelJobRequest]
    ) -> models.CancelJobResponse:
        """Cancel the jobs.

        Args:
            job_ids: List of CancelJobRequest.

        Returns:
            The errors that appear while attempting the operation.

        Raises:
            ApiException: if unable to communicate with the System Service
                or provided an invalid argument.
        """
        ...
