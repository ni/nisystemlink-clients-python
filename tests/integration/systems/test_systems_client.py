import pytest
from typing import List, Generator, Callable

from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.systems import SystemsClient
from nisystemlink.clients.systems.models import (
    CreateJobResponse,
    CreateJobRequest,
    JobSummaryResponse,
    QueryJobsRequest,
    CancelJobRequest,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> SystemsClient:
    """Fixture to create an SystemsClient instance."""
    return SystemsClient(enterprise_config)


@pytest.fixture(scope="class")
def create_job(
    client: SystemsClient,
):
    """Fixture to create a job."""
    responses: List[CreateJobResponse] = []

    def _create_job(job: CreateJobRequest) -> CreateJobResponse:
        response = client.create_job(job)
        responses.append(response)
        return response

    yield _create_job

    from nisystemlink.clients.systems.models import CancelJobRequest

    job_requests = [
        CancelJobRequest(jid=response.jid, tgt=response.tgt[0])
        for response in responses
        if response.tgt is not None
    ]

    client.cancel_jobs(job_requests)


@pytest.fixture(scope="class")
def create_multiple_jobs(
    create_job,
):
    """Fixture to create multiple jobs."""
    responses = []
    arg_1 = [["A description"]]
    arg_2 = [["Another description"]]
    tgt = ["HVM_domU--SN-ec200972-eeca-062e-5bf5-33g3g3g3d73b2--MAC-0A-E1-20-D6-96-2B"]
    fun_1 = ["system.set_computer_desc"]
    fun_2 = ["system.set_computer_asc"]
    metadata = {"queued": True, "refresh_minion_cache": {"grains": True}}
    job_1 = CreateJobRequest(
        arg=arg_1,
        tgt=tgt,
        fun=fun_1,
        metadata=metadata,
    )
    responses.append(create_job(job_1))

    job_2 = CreateJobRequest(
        arg=arg_2,
        tgt=tgt,
        fun=fun_2,
        metadata=metadata,
    )
    responses.append(create_job(job_2))

    return responses


@pytest.mark.integration
@pytest.mark.enterprise
class TestSystemsClient:
    def test__create_job__succeeds(
        self,
        create_job,
    ):
        arg = [["A description"]]
        tgt = [
            "HVM_domU--SN-ec200972-eeca-062e-5bf5-017a25451b39--MAC-0A-E1-20-D6-96-2B"
        ]
        fun = ["system.set_computer_desc"]
        metadata = {"queued": True, "refresh_minion_cache": {"grains": True}}
        job = CreateJobRequest(
            arg=arg,
            tgt=tgt,
            fun=fun,
            metadata=metadata,
        )

        response = create_job(job)

        assert response is not None
        assert response.jid is not None
        assert response.arg == arg
        assert response.tgt == tgt
        assert response.metadata == metadata
        assert response.fun == fun

    def test__list_jobs__single_job__succeeds(self, create_job, client: SystemsClient):
        arg = [["A description"]]
        tgt = [
            "HVM_domU--SN-ec200972-eeca-062e-5bf5-017a25451b39--MAC-0A-E1-20-D6-96-2B"
        ]
        fun = ["system.set_computer_desc"]
        metadata = {"queued": True, "refresh_minion_cache": {"grains": True}}
        job = CreateJobRequest(
            arg=arg,
            tgt=tgt,
            fun=fun,
            metadata=metadata,
        )
        create_job_response = create_job(job)

        response = client.list_jobs(jid=create_job_response.jid)
        assert response is not None
        assert len(response) == 1

        [response_job] = response

        assert response_job.jid == create_job_response.jid
        assert response_job.config is not None
        assert response_job.config.arg == arg
        assert response_job.config.tgt == tgt
        assert response_job.metadata == metadata
        assert response_job.config.fun == fun

    def test__list_jobs__multiple_jobs__succeeds(
        self, create_multiple_jobs, client: SystemsClient
    ):
        response = client.list_jobs(system_id=create_multiple_jobs[0].tgt[0])
        assert response is not None
        assert len(response) == 2

    def test__list_jobs__multiple_jobs_take_one__succeeds(
        self, create_multiple_jobs, client: SystemsClient
    ):
        response = client.list_jobs(system_id=create_multiple_jobs[0].tgt[0], take=1)
        assert response is not None
        assert len(response) == 1

    def test__list_jobs__multiple_jobs_skip_one__succeeds(
        self, create_multiple_jobs, client: SystemsClient
    ):
        response = client.list_jobs(system_id=create_multiple_jobs[0].tgt[0], skip=1)
        assert response is not None
        assert len(response) == 1

    def test__list_jobs__Invalid_system_id__fails(self, client: SystemsClient):
        with pytest.raises(Exception):
            client.list_jobs(system_id="Invalid_system_id")

    def test__list_jobs__Invalid_jid__fails(self, client: SystemsClient):
        with pytest.raises(Exception):
            client.list_jobs(jid="Invalid_jid")

    def test__get_job_summary__succeeds(self, client: SystemsClient):
        response = client.get_job_summary()

        assert response is not None
        assert isinstance(response, JobSummaryResponse)

    def test__query_jobs__take_filter__succeeds(self, client: SystemsClient):
        query = QueryJobsRequest(take=1)
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.count is not None
        assert response.data is not None
        assert isinstance(response.data, list)
        assert response.count == 1

    def test__query_jobs__config_fun_filter__succeeds(self, client: SystemsClient):
        query = QueryJobsRequest(
            filter='config.fun.Contains("system.set_computer_desc")'
        )
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.count is not None
        assert response.data is not None
        assert isinstance(response.data, list)
        assert response.count > 0

    def test__query_jobs__config_jid_filter__succeeds(
        self, create_multiple_jobs, client: SystemsClient
    ):
        query = QueryJobsRequest(filter=f"jid={create_multiple_jobs[0].jid}")
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.count is not None
        assert response.data is not None
        assert isinstance(response.data, list)
        assert response.count == 1

    def test__cancel_jobs__single_job__succeeds(self, client: SystemsClient):
        arg = [["A description"]]
        tgt = [
            "HVM_domU--SN-ec200972-eeca-062e-5bf5-017a25451b39--MAC-0A-E1-20-D6-96-2B"
        ]
        fun = ["system.set_computer_desc"]
        metadata = {"queued": True, "refresh_minion_cache": {"grains": True}}
        job = CreateJobRequest(
            arg=arg,
            tgt=tgt,
            fun=fun,
            metadata=metadata,
        )
        response = client.create_job(job)

        cancel_job_request = CancelJobRequest(jid=response.jid, tgt=tgt[0])
        cancel_response = client.cancel_jobs([cancel_job_request])

        assert cancel_response.error is None

    def test__cancel_jobs__multiple_job__succeeds(self, client: SystemsClient):
        arg_1 = [["A description"]]
        arg_2 = [["Another description"]]
        tgt = [
            "HVM_domU--SN-ec200972-eeca-062e-5bf5-017a25451b39--MAC-0A-E1-20-D6-96-2B"
        ]
        fun = ["system.set_computer_desc"]
        metadata = {"queued": True, "refresh_minion_cache": {"grains": True}}
        job_1 = CreateJobRequest(
            arg=arg_1,
            tgt=tgt,
            fun=fun,
            metadata=metadata,
        )
        response_1 = client.create_job(job_1)
        job_2 = CreateJobRequest(
            arg=arg_2,
            tgt=tgt,
            fun=fun,
            metadata=metadata,
        )
        response_2 = client.create_job(job_2)

        cancel_job_request_1 = CancelJobRequest(jid=response_1.jid, tgt=tgt[0])
        cancel_job_request_2 = CancelJobRequest(jid=response_2.jid, tgt=tgt[0])
        cancel_response = client.cancel_jobs(
            [cancel_job_request_1, cancel_job_request_2]
        )

        assert cancel_response.error is None

    def test__cancel_jobs__Invalid_jid__fails(self, client: SystemsClient):
        cancel_job_request = CancelJobRequest(jid="Invalid_jid", tgt="Invalid_tgt")
        cancel_response = client.cancel_jobs([cancel_job_request])

        assert cancel_response.error is not None
        assert cancel_response.error.message is not None
