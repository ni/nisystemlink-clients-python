from typing import List

import pytest
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.system import SystemClient
from nisystemlink.clients.system.models import (
    CancelJobRequest,
    CreateJobRequest,
    CreateJobResponse,
    QueryJobsRequest,
)

TARGET_SYSTEM = (
    # "HVM_domU--SN-ec200972-eeca-062e-5bf5-33g3g3g3d73b2--MAC-0A-E1-20-D6-96-2B"
    "20UAS1L61D--SN-PF2K5S1M--MAC-8C-8C-AA-82-6A-F8"
)
METADATA = {"queued": True, "refresh_minion_cache": {"grains": True}}
SAMPLE_FUN_1 = "system.sample_function_one"
SAMPLE_FUN_2 = "system.sample_function_two"


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> SystemClient:
    """Fixture to create an SystemClient instance."""
    return SystemClient(enterprise_config)


@pytest.fixture(scope="class")
def create_job(
    client: SystemClient,
):
    """Fixture to create a job."""
    responses: List[CreateJobResponse] = []

    def _create_job(job: CreateJobRequest) -> CreateJobResponse:
        response = client.create_job(job)
        responses.append(response)
        return response

    yield _create_job

    job_requests = [
        CancelJobRequest(id=response.id, system_id=TARGET_SYSTEM)
        for response in responses
        if response.id != ""
    ]

    if len(job_requests):
        client.cancel_jobs(job_requests)


@pytest.fixture(scope="class", autouse=True)
def create_multiple_jobs(
    create_job,
):
    """Fixture to create multiple jobs."""
    responses = []
    arg_1 = [["sample argument one"]]
    arg_2 = [["sample argument two"]]
    tgt = [TARGET_SYSTEM]
    fun_1 = [SAMPLE_FUN_1]
    fun_2 = [SAMPLE_FUN_2]

    metadata = METADATA

    job_1 = CreateJobRequest(
        arguments=arg_1,
        target_systems=tgt,
        functions=fun_1,
        metadata=metadata,
    )
    responses.append(create_job(job_1))

    job_2 = CreateJobRequest(
        arguments=arg_2,
        target_systems=tgt,
        functions=fun_2,
        metadata=metadata,
    )
    responses.append(create_job(job_2))

    job_3 = CreateJobRequest(
        arguments=arg_1,
        target_systems=tgt,
        functions=fun_2,
        metadata=metadata,
    )
    responses.append(create_job(job_3))

    return responses


@pytest.mark.integration
@pytest.mark.enterprise
class TestSystemClient:
    def test__create_a_job__job_is_created_with_right_field_values(
        self,
        create_job,
    ):
        arg = [["sample argument"]]
        tgt = [TARGET_SYSTEM]
        fun = ["system.set_computer_desc_sample_function"]

        job = CreateJobRequest(
            arguments=arg,
            target_systems=tgt,
            functions=fun,
            metadata=METADATA,
        )

        response = create_job(job)

        assert response is not None
        assert response.id != ""
        assert response.target_systems == tgt
        assert response.error is None

    def test__get_job_using_target_and_job_id__returns_job_matches_target_and_job_id(
        self, create_multiple_jobs, client: SystemClient
    ):
        [first_job, *_] = create_multiple_jobs
        print(first_job.jid)
        response = client.list_jobs(system_id=TARGET_SYSTEM, jid=first_job.jid)
        assert len(response) == 1
        [response_job] = response
        print(response)
        assert response_job.id == first_job.jid
        assert response_job.config is not None
        assert response_job.config.target_systems == first_job.tgt

    def test__get_jobs_using_target_and_function__return_jobs_match_target_and_function(
        self, create_multiple_jobs, client: SystemClient
    ):
        [_, second_job, third_job] = create_multiple_jobs
        response = client.list_jobs(system_id=TARGET_SYSTEM, function=SAMPLE_FUN_2)
        assert len(response) == 2

        [response_second_job, response_third_job] = response

        assert response_second_job.id == second_job.jid
        assert response_second_job.config is not None
        assert response_second_job.config.target_systems == second_job.tgt

        assert response_third_job.id == third_job.jid
        assert response_third_job.config is not None
        assert response_third_job.config.target_systems == third_job.tgt

    def test__get_job_by_taking_one__return_only_one_job(
        self, create_multiple_jobs, client: SystemClient
    ):
        response = client.list_jobs(system_id=TARGET_SYSTEM, skip=1)
        assert len(response) == 1

    def test__get_jobs_using_invalid_system_id__returns_empty_list(
        self, client: SystemClient
    ):
        response = client.list_jobs(system_id="Invalid_system_id")
        assert len(response) == 0

    def test__get_jobs_using_invalid_jid__returns_empty_list(
        self, client: SystemClient
    ):
        response = client.list_jobs(jid="Invalid_jid")
        assert len(response) == 0

    def test__get_job_summary__returns_job_summary(self, client: SystemClient):
        response = client.get_job_summary()

        assert response is not None
        assert response.active_count is not None
        assert response.failed_count is not None
        assert response.succeeded_count is not None
        assert response.error is None

    def test__query_jobs_by_taking_one__returns_one_job(self, client: SystemClient):
        query = QueryJobsRequest(skip=0, take=1)
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert len(response.data) == response.count == 1

    def test__query_jobs_by_filtering_config__return_jobs_matches_filter(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(skip=0, filter=f"config.fun.Contains({SAMPLE_FUN_2})")
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert response.count is not None
        assert len(response.data) == response.count > 0

    def test__query_jobs_by_filtering_invalid_filter__raises_ApiException(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(
            skip=0, filter='config.fun.Contains("failed_function")'
        )
        with pytest.raises(ApiException):
            client.query_jobs(query=query)

    def test__query_jobs_by_filtering_jid__returns_job_matches_jid(
        self, create_multiple_jobs, client: SystemClient
    ):
        query = QueryJobsRequest(skip=0, filter=f"jid={create_multiple_jobs[0].jid}")
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert len(response.data) == response.count == 1

    def test__query_jobs_by_filtering_invalid_jid__raises_ApiException(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(skip=0, filter="jid=Invalid_jid")
        with pytest.raises(ApiException):
            client.query_jobs(query=query)

    def test__cancel_single_job__cancel_single_job_succeeds(self, client: SystemClient):
        arg = [["sample argument"]]
        tgt = [TARGET_SYSTEM]
        fun = [SAMPLE_FUN_1]
        job = CreateJobRequest(
            arguments=arg,
            target_systems=tgt,
            functions=fun,
            metadata=METADATA,
        )
        response = client.create_job(job)

        cancel_job_request = CancelJobRequest(id=response.id, tgt=TARGET_SYSTEM)
        cancel_response = client.cancel_jobs([cancel_job_request])

        assert cancel_response is None

    def test__cancel_multiple_jobs__cancel_multiple_job_succeeds(
        self, client: SystemClient
    ):
        arg_1 = [["sample argument one"]]
        arg_2 = [["sample argument two"]]
        tgt = [TARGET_SYSTEM]
        fun = [SAMPLE_FUN_2]

        job_1 = CreateJobRequest(
            arguments=arg_1,
            target_systems=tgt,
            functions=fun,
            metadata=METADATA,
        )
        response_1 = client.create_job(job_1)
        job_2 = CreateJobRequest(
            arguments=arg_2,
            target_systems=tgt,
            functions=fun,
            metadata=METADATA,
        )
        response_2 = client.create_job(job_2)

        cancel_job_request_1 = CancelJobRequest(id=response_1.id, tgt=TARGET_SYSTEM)
        cancel_job_request_2 = CancelJobRequest(id=response_2.id, tgt=TARGET_SYSTEM)
        cancel_response = client.cancel_jobs(
            [cancel_job_request_1, cancel_job_request_2]
        )

        assert cancel_response is None

    def test__cancel_with_invalid_jid__cancel_job_returns_error(
        self, client: SystemClient
    ):
        cancel_job_request = CancelJobRequest(id="Invalid_jid", tgt="Invalid_tgt")
        cancel_response = client.cancel_jobs([cancel_job_request])

        assert cancel_response is not None
        assert cancel_response.error is not None
        assert cancel_response.error.message is not None
