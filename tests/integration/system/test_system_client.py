import pytest
import responses
import responses.matchers
from nisystemlink.clients.core import ApiError, ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.system import SystemClient
from nisystemlink.clients.system.models import (
    CancelJobRequest,
    CreateJobRequest,
    JobField,
    QueryJobsRequest,
)

TARGET_SYSTEM = "dh33jg-43erhqfb-3r3r3r"
METADATA = {"queued": True, "refresh_minion_cache": {"grains": True}}
SAMPLE_FUN_1 = "system.sample_function_one"
SAMPLE_FUN_2 = "system.sample_function_two"


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> SystemClient:
    """Fixture to create an SystemClient instance."""
    return SystemClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestSystemClient:
    @responses.activate
    def test__create_a_job__job_is_created_with_right_field_values(
        self,
        client: SystemClient,
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
        job_id = "sample_job_id"

        return_value = {
            "jid": job_id,
            "tgt": job.target_systems,
            "fun": job.functions,
            "arg": job.arguments,
            "metadata": job.metadata,
            "error": None,
        }

        responses.add(
            method=responses.POST,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/jobs",
            json=return_value,
            status=201,
        )

        response = client.create_job(job)

        assert response is not None
        assert response.id == job_id
        assert response.target_systems == tgt
        assert response.error is None

    @responses.activate
    def test__create_job_with_invalid_target_system__return_error_response(
        self,
        client: SystemClient,
    ):
        arg = [["sample argument"]]
        tgt = ["Invalid_target_system"]
        fun = ["system.set_computer_desc_sample_function"]

        job = CreateJobRequest(
            arguments=arg,
            target_systems=tgt,
            functions=fun,
            metadata=METADATA,
        )

        return_value = {
            "jid": "",
            "tgt": job.target_systems,
            "fun": job.functions,
            "arg": job.arguments,
            "metadata": job.metadata,
            "error": {
                "name": "Skyline.OneOrMoreErrorsOccurred",
                "code": -251041,
                "message": "One or more errors occurred. See the contained list for details of each error.",
                "args": [],
                "innerErrors": [
                    {
                        "name": "SystemsManagement.SystemNotFound",
                        "code": -254010,
                        "message": "System not found.",
                        "resourceType": "Minion",
                        "resourceId": "Invalid_target_system",
                        "args": ["Invalid_target_system"],
                        "innerErrors": [],
                    }
                ],
            },
        }

        responses.add(
            method=responses.POST,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/jobs",
            json=return_value,
            status=201,
        )

        response = client.create_job(job)

        assert response is not None
        assert response.id == ""
        assert response.target_systems == tgt
        assert response.error is not None

    @responses.activate
    def test__get_job_using_target_and_job_id__returns_job_matches_target_and_job_id(
        self,
        client: SystemClient,
    ):
        job_id = "sample_job_id"
        return_value = [
            {
                "jid": job_id,
                "id": TARGET_SYSTEM,
                "createdTimestamp": "2024-11-12T06:00:02.212+00:00",
                "lastUpdatedTimestamp": "2024-11-12T11:05:38.614+00:00",
                "state": "CANCELED",
                "config": {
                    "user": "admin",
                    "tgt": [TARGET_SYSTEM],
                    "fun": [SAMPLE_FUN_1],
                },
                "metadata": METADATA,
            },
        ]

        responses.add(
            method=responses.GET,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/jobs",
            json=return_value,
            status=200,
        )

        list_response = client.list_jobs(job_id=job_id, system_id=TARGET_SYSTEM)
        assert len(list_response) == 1
        assert list_response[0].id == job_id
        assert list_response[0].system_id == TARGET_SYSTEM

    @responses.activate
    def test__get_jobs_using_target_and_function__return_jobs_match_target_and_function(
        self, client: SystemClient
    ):
        job_id_1 = "sample_job_id_1"
        job_id_2 = "sample_job_id_2"
        return_value = [
            {
                "jid": job_id_1,
                "id": TARGET_SYSTEM,
                "createdTimestamp": "2024-11-12T06:00:02.212+00:00",
                "lastUpdatedTimestamp": "2024-11-12T11:05:38.614+00:00",
                "state": "CANCELED",
                "config": {
                    "user": "admin",
                    "tgt": [TARGET_SYSTEM],
                    "fun": [SAMPLE_FUN_1],
                },
                "metadata": METADATA,
            },
            {
                "jid": job_id_2,
                "id": TARGET_SYSTEM,
                "createdTimestamp": "2024-11-12T06:00:02.212+00:00",
                "lastUpdatedTimestamp": "2024-11-12T11:05:38.614+00:00",
                "state": "CANCELED",
                "config": {
                    "user": "admin",
                    "tgt": [TARGET_SYSTEM],
                    "fun": [SAMPLE_FUN_1],
                },
                "metadata": METADATA,
            },
        ]

        responses.add(
            method=responses.GET,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/jobs",
            json=return_value,
            status=200,
        )

        list_response = client.list_jobs(system_id=TARGET_SYSTEM, function=SAMPLE_FUN_1)
        assert len(list_response) == 2
        assert list_response[0].id == job_id_1
        assert list_response[1].id == job_id_2

    def test__get_job_by_taking_one__return_only_one_job(self, client: SystemClient):
        response = client.list_jobs(take=1)
        assert len(response) == 1

    def test__get_jobs_using_invalid_system_id__returns_empty_list(
        self, client: SystemClient
    ):
        response = client.list_jobs(system_id="Invalid_system_id")
        assert len(response) == 0

    def test__get_jobs_using_invalid_jid__returns_empty_list(
        self, client: SystemClient
    ):
        response = client.list_jobs(job_id="Invalid_jid")
        assert len(response) == 0

    def test__get_job_summary__returns_job_summary(self, client: SystemClient):
        response = client.get_job_summary()

        assert response is not None
        assert response.active_count is not None
        assert response.failed_count is not None
        assert response.succeeded_count is not None
        assert response.error is None

    def test__query_jobs_by_taking_one__returns_one_job(self, client: SystemClient):
        query = QueryJobsRequest(take=1)
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert len(response.data) == response.count == 1

    @responses.activate
    def test__query_jobs_by_filtering_config__return_jobs_matches_filter(
        self, client: SystemClient
    ):
        job_id = "sample_job_id"
        return_value = {
            "data": [
                {
                    "jid": job_id,
                    "id": TARGET_SYSTEM,
                    "createdTimestamp": "2024-11-12T06:00:02.212+00:00",
                    "lastUpdatedTimestamp": "2024-11-12T11:05:38.614+00:00",
                    "state": "CANCELED",
                    "config": {
                        "user": "admin",
                        "tgt": [TARGET_SYSTEM],
                        "fun": [SAMPLE_FUN_1],
                    },
                    "metadata": METADATA,
                },
            ],
            "count": 1,
        }

        responses.add(
            method=responses.POST,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/query-jobs",
            json=return_value,
            status=200,
        )

        query = QueryJobsRequest(filter=f"config.fun.Contains({SAMPLE_FUN_1})")
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert response.count is not None
        assert len(response.data) == response.count == 1
        assert response.data[0].id == job_id
        assert response.data[0].config is not None
        assert response.data[0].config.functions is not None
        assert response.data[0].config.functions == [SAMPLE_FUN_1]

    def test__query_jobs_by_filtering_invalid_function__returns_empty_list(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(filter='config.fun.Contains("failed_function")')
        response = client.query_jobs(query=query)

        assert response.error is None
        assert response.data is not None
        assert len(response.data) == 0
        assert response.count == 0

    @responses.activate
    def test__query_jobs_by_filtering_job_id__returns_job_matches_job_id(
        self, client: SystemClient
    ):
        job_id = "sample_job_id"
        return_value = {
            "data": [
                {
                    "jid": job_id,
                    "id": TARGET_SYSTEM,
                    "createdTimestamp": "2024-11-12T06:00:02.212+00:00",
                    "lastUpdatedTimestamp": "2024-11-12T11:05:38.614+00:00",
                    "state": "CANCELED",
                    "config": {
                        "user": "admin",
                        "tgt": [TARGET_SYSTEM],
                        "fun": [SAMPLE_FUN_1],
                    },
                    "metadata": METADATA,
                },
            ],
            "count": 1,
        }

        responses.add(
            method=responses.POST,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/query-jobs",
            json=return_value,
            status=200,
        )
        query = QueryJobsRequest(filter=f"jid={job_id}")
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert len(response.data) == response.count == 1
        assert response.data[0].id == job_id

    def test__query_jobs_by_filtering_invalid_job_id__raises_ApiException_BadRequest(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(filter="jid=Invalid_jid")
        with pytest.raises(ApiException, match="Bad Request"):
            client.query_jobs(query=query)

    def test__query_jobs_by_filtering_invalid_system_id__raises_ApiException(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(filter="id=Invalid_system_id")
        with pytest.raises(ApiException, match="Bad Request"):
            client.query_jobs(query=query)

    def test__query_jobs_by_projecting_job_id_and_system_id__returns_jobs_with_only_job_id_and_system_id_properties(
        self,
        client: SystemClient,
    ):
        query = QueryJobsRequest(projection=[JobField.ID, JobField.SYSTEM_ID], take=3)
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert len(response.data) == response.count == 3

        assert all(
            job.id is not None
            and job.system_id is not None
            and job.created_timestamp is None
            and job.last_updated_timestamp is None
            and job.state is None
            and job.config is None
            and job.metadata is None
            and job.result is None
            for job in response.data
        )

    def test__query_jobs_with_invalid_projection__raises_ApiException_BadRequest(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(projection=["Invalid_projection"], take=3)
        with pytest.raises(ApiException, match="Bad Request"):
            client.query_jobs(query=query)

    def test__query_jobs_order_by_created_timestamp_in_asc__returns_jobs_sorted_by_created_timestamp_in_asc(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(order_by=JobField.CREATED_TIMESTAMP, take=3)
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert len(response.data) == response.count == 3

        assert response.data[0].created_timestamp is not None
        assert response.data[1].created_timestamp is not None
        assert response.data[2].created_timestamp is not None

        assert (
            response.data[0].created_timestamp
            <= response.data[1].created_timestamp
            <= response.data[2].created_timestamp
        )

    def test__query_jobs_order_by_completing_timestamp_in_desc__returns_jobs_sorted_by_completing_timestamp_in_desc(
        self, client: SystemClient
    ):
        query = QueryJobsRequest(
            order_by=JobField.COMPLETING_TIMESTAMP, descending=True, take=3
        )
        response = client.query_jobs(query=query)

        assert response is not None
        assert response.data is not None
        assert len(response.data) == response.count == 3

        assert response.data[0].completing_timestamp is not None
        assert response.data[1].completing_timestamp is not None
        assert response.data[2].completing_timestamp is not None

        assert (
            response.data[0].completing_timestamp
            >= response.data[1].completing_timestamp
            >= response.data[2].completing_timestamp
        )

    @responses.activate
    def test__cancel_single_job__cancel_single_job_succeeds(self, client: SystemClient):
        responses.add(
            method=responses.POST,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/cancel-jobs",
            status=200,
        )

        cancel_job_request = CancelJobRequest(id="Job.id", system_id=TARGET_SYSTEM)
        cancel_response = client.cancel_jobs([cancel_job_request])

        assert cancel_response is None

    @responses.activate
    def test__cancel_multiple_jobs__cancel_multiple_job_succeeds(
        self, client: SystemClient
    ):

        responses.add(
            method=responses.POST,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/cancel-jobs",
            status=200,
        )

        cancel_job_request_1 = CancelJobRequest(id="Job_1.id", system_id=TARGET_SYSTEM)
        cancel_job_request_2 = CancelJobRequest(id="Job_2.id", system_id=TARGET_SYSTEM)
        cancel_response = client.cancel_jobs(
            [cancel_job_request_1, cancel_job_request_2]
        )

        assert cancel_response is None

    def test__cancel_with_invalid_jid_system_id__cancel_job_returns_None(
        self, client: SystemClient
    ):
        cancel_job_request = CancelJobRequest(id="Invalid_jid", system_id="Invalid_tgt")
        cancel_response = client.cancel_jobs([cancel_job_request])

        assert cancel_response is None

    @responses.activate
    def test__cancel_with_invalid_jid_valid_system_id__cancel_job_returns_error(
        self, client: SystemClient
    ):
        return_value = {
            "error": {
                "name": "Skyline.OneOrMoreErrorsOccurred",
                "code": -251041,
                "message": "One or more errors occurred. See the contained list for details of each error.",
                "args": [],
                "innerErrors": [
                    {
                        "name": "SystemsManagement.SaltCancelJobFailed",
                        "code": -254003,
                        "message": "The job is not found or you are not authorized to cancel it.",
                        "resourceType": "Job",
                        "resourceId": "54afefqf4b95-ea89-48df-b21f-dddrwerf56083476",
                        "args": [
                            "54af4b95-ea89-48df-b21f-dddrfrewf56083476",
                            "ferfgertgw--SN-eger--rf-AC-1A-3D-99-75-3F",
                        ],
                        "innerErrors": [],
                    }
                ],
            }
        }

        responses.add(
            method=responses.POST,
            url="https://dev-api.lifecyclesolutions.ni.com/nisysmgmt/v1/cancel-jobs",
            json=return_value,
            status=200,
        )

        cancel_job_request = CancelJobRequest(
            id="Invalid_jid",
            system_id="ferfgertgw--SN-eger--rf-AC-1A-3D-99-75-3F",
        )
        cancel_response = client.cancel_jobs([cancel_job_request])

        assert isinstance(cancel_response, ApiError)
