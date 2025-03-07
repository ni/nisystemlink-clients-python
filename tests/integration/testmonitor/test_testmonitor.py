import uuid
from typing import Dict, List, Optional

import pytest
from nisystemlink.clients.core._api_exception import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateResultRequest,
    CreateResultsPartialSuccess,
    CreateStepRequest,
    CreateStepsPartialSuccess,
    PagedSteps,
    QueryStepsRequest,
    QueryStepValuesRequest,
    Result,
    Status,
    Step,
    StepField,
    StepIdResultIdPair,
    UpdateResultRequest,
    UpdateStepRequest,
    UpdateStepsPartialSuccess,
)
from nisystemlink.clients.testmonitor.models._named_value import NamedValue
from nisystemlink.clients.testmonitor.models._paged_results import PagedResults
from nisystemlink.clients.testmonitor.models._query_results_request import (
    QueryResultsRequest,
    QueryResultValuesRequest,
    ResultField,
)
from nisystemlink.clients.testmonitor.models._step_data import Measurement, StepData


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestMonitorClient:
    """Fixture to create a TestMonitorClient instance."""
    return TestMonitorClient(enterprise_config)


@pytest.fixture
def unique_identifier() -> str:
    """Unique result/step id for this test."""
    unique_id = uuid.uuid1().hex
    return unique_id


@pytest.fixture
def create_results(client: TestMonitorClient):
    """Fixture to return a factory that creates results."""
    responses: List[CreateResultsPartialSuccess] = []

    def _create_results(
        results: List[CreateResultRequest],
    ) -> CreateResultsPartialSuccess:
        response = client.create_results(results)
        responses.append(response)
        return response

    yield _create_results

    created_results: List[Result] = []
    for response in responses:
        if response.results:
            created_results = created_results + response.results
    client.delete_results(ids=[str(result.id) for result in created_results])


@pytest.fixture
def create_steps(client: TestMonitorClient):
    """Fixture to return a factory that creates steps."""
    responses: List[CreateStepsPartialSuccess] = []

    def _create_steps(
        steps: List[CreateStepRequest],
    ) -> CreateStepsPartialSuccess:
        response = client.create_steps(steps)
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


@pytest.mark.integration
@pytest.mark.enterprise
class TestTestMonitor:
    def test__api_info__returns(self, client: TestMonitorClient):
        response = client.api_info()
        assert len(response.dict()) != 0

    def test__create_single_result__one_result_created_with_right_field_values(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        keywords = ["testing"]
        properties = {"test_property": "yes"}
        program_name = "Test Program"
        status = Status.PASSED()
        host_name = "Test Host"
        system_id = "Test System"
        serial_number = "Test Serial Number"
        result = CreateResultRequest(
            part_number=part_number,
            keywords=keywords,
            properties=properties,
            program_name=program_name,
            status=status,
            host_name=host_name,
            system_id=system_id,
            serial_number=serial_number,
        )

        response: CreateResultsPartialSuccess = create_results([result])

        assert response is not None
        assert len(response.results) == 1
        created_result = response.results[0]
        assert created_result.part_number == part_number
        assert created_result.keywords == keywords
        assert created_result.properties == properties
        assert created_result.program_name == program_name
        assert created_result.status == status
        assert created_result.host_name == host_name
        assert created_result.system_id == system_id
        assert created_result.serial_number == serial_number

    def test__create_multiple_results__multiple_creates_succeed(
        self, client: TestMonitorClient, create_results
    ):
        program_name = "Test Program"
        status = Status.PASSED()
        results = [
            CreateResultRequest(
                part_number=uuid.uuid1().hex, program_name=program_name, status=status
            ),
            CreateResultRequest(
                part_number=uuid.uuid1().hex, program_name=program_name, status=status
            ),
        ]

        response: CreateResultsPartialSuccess = create_results(results)

        assert response is not None
        assert len(response.results) == 2

    def test__create_single_result_and_get_results__at_least_one_result_exists(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        program_name = "Test Program"
        status = Status.PASSED()
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name=program_name,
                status=status,
                properties={"test": None},
            )
        ]
        create_results(results)

        get_response = client.get_results()

        assert get_response is not None
        assert len(get_response.results) >= 1

    def test__create_multiple_results_and_get_results_with_take__only_take_returned(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        program_name = "Test Program"
        status = Status.PASSED()
        results = [
            CreateResultRequest(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
            CreateResultRequest(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
        ]
        create_results(results)

        get_response = client.get_results(take=1)

        assert get_response is not None
        assert len(get_response.results) == 1

    def test__create_multiple_results_and_get_results_with_count_at_least_one_count(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        program_name = "Test Program"
        status = Status.PASSED()
        results = [
            CreateResultRequest(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
            CreateResultRequest(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
        ]
        create_results(results)

        get_response: PagedResults = client.get_results(return_count=True)

        assert get_response is not None
        assert get_response.total_count is not None and get_response.total_count >= 2

    def test__get_result_by_id__result_matches_expected(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        program_name = "Test Program"
        status = Status.PASSED()
        results = [
            CreateResultRequest(
                part_number=part_number, program_name=program_name, status=status
            )
        ]

        create_response: CreateResultsPartialSuccess = create_results(results)

        assert create_response is not None
        id = str(create_response.results[0].id)
        result = client.get_result(id)
        assert result is not None
        assert result.part_number == part_number
        assert result.program_name == program_name
        assert result.status == status

    def test__query_result_by_part_number__matches_expected(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        program_name = "Test Program"
        status = Status.PASSED()
        results = [
            CreateResultRequest(
                part_number=part_number, program_name=program_name, status=status
            )
        ]

        create_response: CreateResultsPartialSuccess = create_results(results)

        assert create_response is not None
        query_request = QueryResultsRequest(
            filter=f'partNumber="{part_number}"', return_count=True
        )
        query_response: PagedResults = client.query_results(query_request)
        assert query_response.total_count == 1
        assert query_response.results[0].part_number == part_number

    def test__query_result_values_for_name__name_matches(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        program_name = "Test Program"
        status = Status.PASSED()

        create_response: CreateResultsPartialSuccess = create_results(
            [
                CreateResultRequest(
                    part_number=part_number, program_name=program_name, status=status
                )
            ]
        )
        assert create_response is not None
        query_request = QueryResultValuesRequest(
            filter=f'partNumber="{part_number}"', field=ResultField.PROGRAM_NAME
        )
        query_response: List[str] = client.query_result_values(query_request)

        assert query_response is not None
        assert len(query_response) == 1
        assert query_response[0] == program_name

    def test__update_keywords_with_replace__keywords_replaced(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        original_keyword = "originalKeyword"
        updated_keyword = "updatedKeyword"
        program_name = "Test Program"
        status = Status.PASSED()
        create_response: CreateResultsPartialSuccess = create_results(
            [
                CreateResultRequest(
                    part_number=unique_identifier,
                    keywords=[original_keyword],
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = self.__map_result_to_update_result_request(
            create_response.results[0]
        )
        updated_result.keywords = [updated_keyword]
        update_response = client.update_results([updated_result], replace=True)

        assert update_response is not None
        assert len(update_response.results) == 1
        assert (
            update_response.results[0].keywords is not None
            and updated_keyword in update_response.results[0].keywords
        )
        assert original_keyword not in update_response.results[0].keywords

    def test__update_keywords_no_replace__keywords_appended(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        original_keyword = "originalKeyword"
        additional_keyword = "additionalKeyword"
        program_name = "Test Program"
        status = Status.PASSED()
        create_response: CreateResultsPartialSuccess = create_results(
            [
                CreateResultRequest(
                    part_number=unique_identifier,
                    keywords=[original_keyword],
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = self.__map_result_to_update_result_request(
            create_response.results[0]
        )
        updated_result.keywords = [additional_keyword]
        update_response = client.update_results([updated_result], replace=False)

        assert update_response is not None
        assert len(update_response.results) == 1
        assert (
            update_response.results[0].keywords is not None
            and original_keyword in update_response.results[0].keywords
        )
        assert (
            update_response.results[0].keywords is not None
            and additional_keyword in update_response.results[0].keywords
        )

    def test__update_properties_with_replace__properties_replaced(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        new_key = "newKey"
        original_properties = {"originalKey": "originalValue"}
        program_name = "Test Program"
        status = Status.PASSED()
        new_properties: Dict[str, Optional[str]] = {new_key: "newValue"}
        create_response: CreateResultsPartialSuccess = create_results(
            [
                CreateResultRequest(
                    part_number=unique_identifier,
                    properties=original_properties,
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = self.__map_result_to_update_result_request(
            create_response.results[0]
        )
        updated_result.properties = new_properties
        update_response = client.update_results([updated_result], replace=True)

        assert update_response is not None
        assert len(update_response.results) == 1
        assert (
            update_response.results[0].properties is not None
            and len(update_response.results[0].properties) == 1
        )
        assert new_key in update_response.results[0].properties.keys()
        assert update_response.results[0].properties[new_key] == new_properties[new_key]

    def test__update_properties_append__properties_appended(
        self, client: TestMonitorClient, create_results, unique_identifier
    ):
        original_key = "originalKey"
        new_key = "newKey"
        original_properties = {original_key: "originalValue"}
        program_name = "Test Program"
        status = Status.PASSED()
        new_properties: Dict[str, Optional[str]] = {new_key: "newValue"}
        create_response: CreateResultsPartialSuccess = create_results(
            [
                CreateResultRequest(
                    part_number=unique_identifier,
                    properties=original_properties,
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = self.__map_result_to_update_result_request(
            create_response.results[0]
        )
        updated_result.properties = new_properties
        update_response = client.update_results([updated_result], replace=False)

        assert update_response is not None
        assert len(update_response.results) == 1
        updated_result = self.__map_result_to_update_result_request(
            update_response.results[0]
        )
        assert (
            updated_result.properties is not None
            and len(updated_result.properties) == 2
        )
        assert original_key in updated_result.properties.keys()
        assert new_key in updated_result.properties.keys()
        assert (
            updated_result.properties[original_key] == original_properties[original_key]
        )
        assert updated_result.properties[new_key] == new_properties[new_key]

    def __map_result_to_update_result_request(
        self, result: Result
    ) -> UpdateResultRequest:
        result_dict = result.dict(exclude={"status_type_summary", "updated_at"})
        return UpdateResultRequest(**result_dict)

    def test__create_single_step__creation_succeed(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        step_id = unique_identifier
        result_id = created_result.results[0].id
        name = "Test Step 1"
        data = StepData(
            text="This is a test step",
            parameters=[Measurement(name="param1", measurement="10")],
        )
        properties = {"property1": "value1", "property2": "value2"}
        keywords = ["keyword1", "keyword2"]
        inputs = [NamedValue(name="input1", value="inputValue1")]
        step = CreateStepRequest(
            step_id=step_id,
            result_id=result_id,
            name=name,
            data=data,
            properties=properties,
            keywords=keywords,
            inputs=inputs,
        )

        response: CreateStepsPartialSuccess = create_steps(steps=[step])

        assert response is not None
        assert len(response.steps) == 1
        created_step = response.steps[0]
        assert created_step.step_id == step_id
        assert created_step.result_id == result_id
        assert created_step.name == name
        assert created_step.data == data
        assert created_step.properties == properties
        assert created_step.keywords == keywords
        assert created_step.inputs == inputs
        assert not created_step.outputs

    def test__create_multiple_steps__multiple_creation_succeed(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        steps = [
            CreateStepRequest(
                step_id=uuid.uuid1().hex,
                result_id=result_id,
                name="Step 1",
            ),
            CreateStepRequest(
                step_id=uuid.uuid1().hex,
                result_id=result_id,
                name="Step 2",
            ),
        ]

        response: CreateStepsPartialSuccess = create_steps(steps)

        assert response is not None
        assert len(response.steps) == 2

    def test__create_multiple_steps_with_children__multiple_creation_succeed(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        parent_step_id = uuid.uuid1().hex
        steps = [
            CreateStepRequest(
                step_id=parent_step_id,
                result_id=result_id,
                name="Step 1",
                children=[
                    CreateStepRequest(
                        step_id=uuid.uuid1().hex,
                        result_id=result_id,
                        name="Step 2",
                    ),
                ],
            ),
        ]

        response: CreateStepsPartialSuccess = create_steps(steps)

        assert response is not None
        assert len(response.steps) == 2
        child_step = response.steps[1]
        assert child_step is not None
        assert child_step.parent_id == parent_step_id

    def test__get_steps__at_least_one_step_exists(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        steps = [
            CreateStepRequest(
                step_id=unique_identifier,
                result_id=result_id,
                name="Step 1",
            )
        ]
        create_steps(steps)

        get_response = client.get_steps()

        assert get_response is not None
        assert len(get_response.steps) >= 1

    def test_with_multiple_steps__get_steps_with_take__only_take_returned(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        steps = [
            CreateStepRequest(
                step_id=unique_identifier,
                result_id=result_id,
                name="Step 1",
            ),
            CreateStepRequest(
                step_id=unique_identifier,
                result_id=result_id,
                name="Step 2",
            ),
        ]
        create_steps(steps)

        get_response = client.get_steps(take=1)

        assert get_response is not None
        assert len(get_response.steps) == 1

    def test__get_steps_with_return_count__steps_and_count_returned(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        steps = [
            CreateStepRequest(
                step_id=unique_identifier,
                result_id=result_id,
                name="Step 1",
            ),
            CreateStepRequest(
                step_id=unique_identifier,
                result_id=result_id,
                name="Step 2",
            ),
        ]
        create_steps(steps)

        get_response: PagedSteps = client.get_steps(return_count=True, take=5)

        assert get_response is not None
        assert get_response.total_count is not None and get_response.total_count >= 2

    def test__get_step_by_id__expected_step_returned(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        step_id = unique_identifier
        steps = [CreateStepRequest(step_id=step_id, result_id=result_id, name="Step 1")]
        create_response: CreateStepsPartialSuccess = create_steps(steps)
        assert create_response is not None

        step: Step = client.get_step(result_id=result_id, step_id=step_id)

        assert step is not None
        assert step.step_id == step_id
        assert step.result_id == result_id

    def test__query_step_by_name_and_result_id__expected_step_returned(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        step_id = unique_identifier
        step_name = "Step 1"
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
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        step_id = unique_identifier
        step_name = "query values test"
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
        assert query_response[0] == step_name

    def test__update_step_data_and_inputs__data_and_inputs_updated(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        step_id = unique_identifier
        create_response: CreateStepsPartialSuccess = create_steps(
            [
                CreateStepRequest(
                    step_id=step_id,
                    result_id=result_id,
                    name="My Step",
                    data=StepData(
                        text="My output string",
                        parameters=[
                            Measurement(
                                name="Current",
                                status="Passed",
                                measurement="3.725",
                                lowLimit="3.65",
                                highLimit="3.8",
                                units="A",
                                comparisonType="GELE",
                            )
                        ],
                    ),
                    inputs=[
                        NamedValue(name="Temperature", value="35"),
                        NamedValue(name="Voltage", value="5"),
                    ],
                    outputs=[
                        NamedValue(name="Current", value="3.725"),
                    ],
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.steps) == 1
        step = create_response.steps[0]

        updated_data = StepData(
            text="My updated output string",
            parameters=[
                Measurement(
                    name="Voltage",
                    status="Passed",
                    measurement="3.725",
                    lowLimit="3.65",
                    highLimit="3.8",
                    units="V",
                    comparisonType="GELE",
                    specId="spec_01",
                    specInfo={"specKey": "specValue"},
                )
            ],
        )
        updated_inputs = [
            NamedValue(name="Temperature", value="40"),
            NamedValue(name="Voltage", value="10"),
        ]
        updated_outputs = [NamedValue(name="Current", value="4.725")]
        update_response: UpdateStepsPartialSuccess = client.update_steps(
            steps=[
                UpdateStepRequest(
                    step_id=step.step_id,
                    result_id=step.result_id,
                    data=updated_data,
                    inputs=updated_inputs,
                    outputs=updated_outputs,
                )
            ]
        )

        assert update_response is not None
        assert update_response.steps is not None
        assert len(update_response.steps) == 1
        assert update_response.steps[0].inputs == updated_inputs
        assert update_response.steps[0].outputs == updated_outputs
        assert update_response.steps[0].data is not None
        assert update_response.steps[0].data.text == updated_data.text
        assert update_response.steps[0].data.parameters is not None
        assert updated_data.parameters is not None
        assert len(update_response.steps[0].data.parameters) == 1
        updated_measurement = update_response.steps[0].data.parameters[0]
        assert updated_measurement.name == updated_data.parameters[0].name
        assert updated_measurement.status == updated_data.parameters[0].status
        assert (
            updated_measurement.measurement
            == updated_data.parameters[0].measurement
        )
        assert updated_measurement.lowLimit == updated_data.parameters[0].lowLimit
        assert updated_measurement.highLimit == updated_data.parameters[0].highLimit
        assert updated_measurement.units == updated_data.parameters[0].units
        assert (
            updated_measurement.comparisonType
            == updated_data.parameters[0].comparisonType
        )
        assert updated_measurement.dict().get("specId") == updated_data.parameters[0].dict().get("specId")
        assert getattr(updated_measurement, "specInfo", None) == updated_data.parameters[0].dict().get("specInfo")

    def test__update_step_with_replace_true__replace_keywords_and_properties(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        step_id = unique_identifier
        create_response: CreateStepsPartialSuccess = create_steps(
            [
                CreateStepRequest(
                    step_id=step_id,
                    result_id=result_id,
                    name="Original Name",
                    properties={"originalProperty": "originalValue"},
                    keywords=["originalKeyword"],
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.steps) == 1
        step = create_response.steps[0]

        new_properties = {"property1": "value1", "property2": "value2"}
        new_keywords = ["keyword1", "keyword2"]
        update_response: UpdateStepsPartialSuccess = client.update_steps(
            steps=[
                UpdateStepRequest(
                    step_id=step.step_id,
                    result_id=step.result_id,
                    keywords=new_keywords,
                    properties=new_properties,
                )
            ],
            replace_keywords=True,
            replace_properties=True,
        )

        assert update_response is not None
        assert len(update_response.steps) == 1
        assert update_response.steps[0].keywords == new_keywords
        assert update_response.steps[0].properties == new_properties

    def test__delete_existing_step__deleted(
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
        step_id = unique_identifier
        steps = [
            CreateStepRequest(
                step_id=step_id,
                result_id=result_id,
                name="Step 1",
            )
        ]
        create_response: CreateStepsPartialSuccess = create_steps(steps)
        assert create_response.steps
        created_step = create_response.steps[0]

        assert created_step.step_id is not None
        assert created_step.result_id is not None
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
        self, client: TestMonitorClient, create_results, create_steps, unique_identifier
    ):
        results = [
            CreateResultRequest(
                part_number=unique_identifier,
                program_name="Test Program",
                status=Status.PASSED(),
            )
        ]
        created_result = create_results(results)
        result_id = created_result.results[0].id
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
            steps=[
                StepIdResultIdPair(step_id=step.step_id, result_id=step.result_id)
                for step in created_steps
            ]
        )

        assert delete_response is None
