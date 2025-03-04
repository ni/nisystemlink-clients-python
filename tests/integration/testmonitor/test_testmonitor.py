import uuid
from typing import List

import pytest
from nisystemlink.clients.core._api_exception import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    # CreateResultRequest,
    # CreateResultsPartialSuccess,
    CreateStepRequest,
    CreateStepsPartialSuccess,
    CreateStepsRequest,
    PagedSteps,
    QueryStepsRequest,
    QueryStepValuesRequest,
    # Result,
    # Status,
    Step,
    StepField,
    StepIdResultIdPair,
    UpdateStepRequest,
    UpdateStepsPartialSuccess,
    UpdateStepsRequest,
)
from nisystemlink.clients.testmonitor.models._step import StepDataObject


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestMonitorClient:
    """Fixture to create a TestMonitorClient instance."""
    return TestMonitorClient(enterprise_config)


@pytest.fixture
def unique_identifier() -> str:
    """Unique step id for this test."""
    unique_id = uuid.uuid1().hex
    return unique_id


@pytest.fixture
def create_steps(client: TestMonitorClient):
    """Fixture to return a factory that creates steps."""
    responses: List[CreateStepsPartialSuccess] = []

    def _create_steps(
        steps: List[CreateStepRequest],
    ) -> CreateStepsPartialSuccess:
        response = client.create_steps(CreateStepsRequest(steps=steps))
        responses.append(response)
        return response

    yield _create_steps

    created_steps: List[Step] = []
    for response in responses:
        if response.steps:
            created_steps = created_steps + response.steps
    client.delete_steps(
        [
            StepIdResultIdPair(step_id=step.step_id, result_id=step.result_id)
            for step in created_steps
        ]
    )


# @pytest.fixture
# def create_result_for_step(client: TestMonitorClient):
#     """Fixture to return a factory that creates results."""
#     responses: List[CreateResultsPartialSuccess] = []

#     def _create_result() -> CreateResultsPartialSuccess:
#         part_number = uuid.uuid1().hex
#         program_name = "Test Program"
#         status = Status.PASSED()
#         host_name = "Test Host"
#         system_id = "Test System"
#         serial_number = "Test Serial Number"
#         result = CreateResultRequest(
#             part_number=part_number,
#             program_name=program_name,
#             status=status,
#             host_name=host_name,
#             system_id=system_id,
#             serial_number=serial_number,
#         )
#         response = client.create_results([result])
#         responses.append(response)
#         return response

#     yield _create_result

#     created_results: List[Result] = []
#     for response in responses:
#         if response.results:
#             created_results = created_results + response.results
#     client.delete_results(ids=[str(result.id) for result in created_results])


@pytest.mark.integration
@pytest.mark.enterprise
class TestTestMonitor:
    def test__api_info__returns(self, client: TestMonitorClient):
        response = client.api_info()
        assert len(response.dict()) != 0

    def test__create_single_step__creation_succeed(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        step_id = unique_identifier
        result_id = "ea6f8d2c-8d57-441e-8375-aa897f59835e"
        name = "Test Step 1"
        data = StepDataObject(
            text="This is a test step", parameters=[{"name": "param1", "value": "10"}]
        )
        properties = {"property1": "value1", "property2": "value2"}
        # createResultResponse: CreateResultsPartialSuccess = create_result()
        # assert createResultResponse is not None
        # assert len(createResultResponse.results) == 1
        # result_id = createResultResponse.results[0].id
        step = CreateStepRequest(
            step_id=step_id,
            result_id=result_id,
            name=name,
            data=data,
            properties=properties,
        )

        response: CreateStepsPartialSuccess = create_steps([step])

        assert response is not None
        assert len(response.steps) == 1
        created_step = response.steps[0]
        assert created_step.step_id == step_id
        assert created_step.result_id == result_id
        assert created_step.name == name
        assert created_step.data == data
        assert created_step.properties == properties
        assert not created_step.inputs
        assert not created_step.outputs

    def test__create_multiple_steps__multiple_creation_succeed(
        self, client: TestMonitorClient, create_steps
    ):
        steps = [
            CreateStepRequest(
                step_id=uuid.uuid1().hex,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 1",
            ),
            CreateStepRequest(
                step_id=uuid.uuid1().hex,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 2",
            ),
        ]

        response: CreateStepsPartialSuccess = create_steps(steps)

        assert response is not None
        assert len(response.steps) == 2

    def test__get_steps__at_least_one_step_exists(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        steps = [
            CreateStepRequest(
                step_id=unique_identifier,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 1",
            )
        ]
        create_steps(steps)

        get_response = client.get_steps()

        assert get_response is not None
        assert len(get_response.steps) >= 1

    def test_with_multiple_steps__get_steps_with_take__only_take_returned(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        steps = [
            CreateStepRequest(
                step_id=unique_identifier,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 1",
            ),
            CreateStepRequest(
                step_id=unique_identifier,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 2",
            ),
        ]
        create_steps(steps)

        get_response = client.get_steps(take=1)

        assert get_response is not None
        assert len(get_response.steps) == 1

    def test__get_steps_with_return_count__steps_and_count_returned(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        steps = [
            CreateStepRequest(
                step_id=unique_identifier,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 1",
            ),
            CreateStepRequest(
                step_id=unique_identifier,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 2",
            ),
        ]
        create_steps(steps)

        get_response: PagedSteps = client.get_steps(return_count=True, take=5)

        assert get_response is not None
        assert get_response.total_count is not None and get_response.total_count >= 2

    def test__get_step_by_id__expected_step_returned(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        step_id = unique_identifier
        result_id = "ea6f8d2c-8d57-441e-8375-aa897f59835e"
        steps = [CreateStepRequest(step_id=step_id, result_id=result_id, name="Step 1")]
        create_response: CreateStepsPartialSuccess = create_steps(steps)
        assert create_response is not None

        step: Step = client.get_step(result_id=result_id, step_id=step_id)

        assert step is not None
        assert step.step_id == step_id
        assert step.result_id == result_id

    def test__query_step_by_name_and_result_id__expected_step_returned(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        step_id = unique_identifier
        step_name = "Step 1"
        result_id = "ea6f8d2c-8d57-441e-8375-aa897f59835e"
        steps = [
            CreateStepRequest(step_id=step_id, result_id=result_id, name=step_name)
        ]
        create_response: CreateStepsPartialSuccess = create_steps(steps)
        assert create_response is not None

        query_request = QueryStepsRequest(
            filter=f'name="{step_name}" & resultId="{result_id}"',
            return_count=False,
            take=5,
        )
        query_response: PagedSteps = client.query_steps(query_request)

        assert query_response is not None
        assert query_response.steps is not None
        assert len(query_response.steps) == 1
        assert query_response.steps[0].step_id == step_id
        assert query_response.steps[0].name == step_name
        assert query_response.steps[0].result_id == result_id

    def test__query_step_values_for_name__name_matches(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        step_id = unique_identifier
        step_name = "query values test"
        result_id = "ea6f8d2c-8d57-441e-8375-aa897f59835e"
        create_response: CreateStepsPartialSuccess = create_steps(
            [CreateStepRequest(step_id=step_id, result_id=result_id, name=step_name)]
        )
        assert create_response is not None
        assert len(create_response.steps) == 1

        query_request = QueryStepValuesRequest(
            filter=f'stepId="{step_id}" & resultId = "{result_id}"',
            field=StepField.NAME,
        )
        query_response: List[str] = client.query_step_values(query_request)

        assert query_response is not None
        assert len(query_response) == 1
        assert query_response[0] == str(step_name)

    def test__update_step_name__name_updated(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        step_id = unique_identifier
        create_response: CreateStepsPartialSuccess = create_steps(
            [
                CreateStepRequest(
                    step_id=step_id,
                    result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                    name="Original Name",
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.steps) == 1
        step = create_response.steps[0]
        new_name = "Updated Name"

        update_response: UpdateStepsPartialSuccess = client.update_steps(
            UpdateStepsRequest(
                steps=[
                    UpdateStepRequest(
                        step_id=step.step_id, result_id=step.result_id, name=new_name
                    )
                ]
            )
        )

        assert update_response is not None
        assert len(update_response.steps) == 1
        assert update_response.steps[0].name == new_name

    def test__delete_existing_step__deleted(
        self, client: TestMonitorClient, create_steps, unique_identifier
    ):
        step_id = unique_identifier
        steps = [
            CreateStepRequest(
                step_id=step_id,
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e",
                name="Step 1",
            )
        ]
        create_response: CreateStepsPartialSuccess = create_steps(steps)
        assert create_response.steps
        created_step = create_response.steps[0]

        delete_response = client.delete_step(
            result_id=created_step.result_id, step_id=created_step.step_id
        )

        assert delete_response is None

    def test__delete_non_existent_step__delete_fails(self, client: TestMonitorClient):
        bad_id = "DEADBEEF"

        with pytest.raises(ApiException, match="InvalidResultOrStepId"):
            client.delete_step(
                result_id="ea6f8d2c-8d57-441e-8375-aa897f59835e", step_id=bad_id
            )

    def test__delete_multiple_steps__deletion_succeed(
        self, client: TestMonitorClient, create_steps
    ):
        result_id = "ea6f8d2c-8d57-441e-8375-aa897f59835e"
        steps = [
            CreateStepRequest(
                step_id=uuid.uuid1().hex, result_id=result_id, name="Step 1"
            ),
            CreateStepRequest(
                step_id=uuid.uuid1().hex, result_id=result_id, name="Step 2"
            ),
        ]
        create_response: CreateStepsPartialSuccess = create_steps(steps)
        assert create_response.steps is not None
        assert len(create_response.steps) == 2
        created_steps = create_response.steps

        delete_response = client.delete_steps(
            [
                StepIdResultIdPair(step_id=step.step_id, result_id=step.result_id)
                for step in created_steps
            ]
        )

        assert delete_response is None
