import uuid
from typing import List

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.result._result_client import ResultClient
from nisystemlink.clients.result.models import (
    Result,
    ResultsPartialSuccess,
    StatusObject,
    StatusType,
)
from nisystemlink.clients.result.models._paged_results import PagedResults
from nisystemlink.clients.result.models._query_results_request import (
    QueryResultsRequest,
    QueryResultValuesRequest,
    ResultField,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> ResultClient:
    """Fixture to create a ResultClient instance."""
    return ResultClient(enterprise_config)


@pytest.fixture
def unique_identifier() -> str:
    """Unique result id for this test."""
    result_id = uuid.uuid1().hex
    return result_id


@pytest.fixture
def create_results(client: ResultClient):
    """Fixture to return a factory that creates results."""
    responses: List[ResultsPartialSuccess] = []

    def _create_results(results: List[Result]) -> ResultsPartialSuccess:
        response = client.create_results(results)
        responses.append(response)
        return response

    yield _create_results

    created_results: List[Result] = []
    for response in responses:
        if response.results:
            created_results = created_results + response.results
    client.delete_results(ids=[str(result.id) for result in created_results])


@pytest.mark.integration
@pytest.mark.enterprise
class TestResultClient:

    def test__create_single_result__one_result_created_with_right_field_values(
        self, client: ResultClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        keywords = ["testing"]
        properties = {"test_property": "yes"}
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        host_name = "Test Host"
        system_id = "Test System"
        serial_number = "Test Serial Number"
        result = Result(
            part_number=part_number,
            keywords=keywords,
            properties=properties,
            program_name=program_name,
            status=status,
            host_name=host_name,
            system_id=system_id,
            serial_number=serial_number,
        )

        response: ResultsPartialSuccess = create_results([result])

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
        self, client: ResultClient, create_results
    ):
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        results = [
            Result(
                part_number=uuid.uuid1().hex, program_name=program_name, status=status
            ),
            Result(
                part_number=uuid.uuid1().hex, program_name=program_name, status=status
            ),
        ]

        response: ResultsPartialSuccess = create_results(results)

        assert response is not None
        assert len(response.results) == 2

    def test__create_single_result_and_get_results__at_least_one_result_exists(
        self, client: ResultClient, create_results, unique_identifier
    ):
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        results = [
            Result(
                part_number=unique_identifier, program_name=program_name, status=status
            )
        ]
        create_results(results)

        get_response = client.get_results_paged()

        assert get_response is not None
        assert len(get_response.results) >= 1

    def test__create_multiple_results_and_get_results_with_take__only_take_returned(
        self, client: ResultClient, create_results, unique_identifier
    ):
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        results = [
            Result(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
            Result(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
        ]
        create_results(results)

        get_response = client.get_results_paged(take=1)

        assert get_response is not None
        assert len(get_response.results) == 1

    def test__create_multiple_results_and_get_results_with_count_at_least_one_count(
        self, client: ResultClient, create_results, unique_identifier
    ):
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        results = [
            Result(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
            Result(
                part_number=unique_identifier, program_name=program_name, status=status
            ),
        ]
        create_results(results)

        get_response: PagedResults = client.get_results_paged(return_count=True)

        assert get_response is not None
        assert get_response.total_count is not None and get_response.total_count >= 2

    def test__get_result_by_id__result_matches_expected(
        self, client: ResultClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        results = [
            Result(part_number=part_number, program_name=program_name, status=status)
        ]

        create_response: ResultsPartialSuccess = create_results(results)

        assert create_response is not None
        id = str(create_response.results[0].id)
        result = client.get_result(id)
        assert result is not None
        assert result.part_number == part_number
        assert result.program_name == program_name
        assert result.status == status

    def test__query_result_by_part_number__matches_expected(
        self, client: ResultClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        results = [
            Result(part_number=part_number, program_name=program_name, status=status)
        ]

        create_response: ResultsPartialSuccess = create_results(results)

        assert create_response is not None
        query_request = QueryResultsRequest(
            filter=f'partNumber="{part_number}"', return_count=True
        )
        query_response: PagedResults = client.query_results_paged(query_request)
        assert query_response.total_count == 1
        assert query_response.results[0].part_number == part_number

    def test__query_result_values_for_name__name_matches(
        self, client: ResultClient, create_results, unique_identifier
    ):
        part_number = unique_identifier
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")

        create_response: ResultsPartialSuccess = create_results(
            [Result(part_number=part_number, program_name=program_name, status=status)]
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
        self, client: ResultClient, create_results, unique_identifier
    ):
        original_keyword = "originalKeyword"
        updated_keyword = "updatedKeyword"
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        create_response: ResultsPartialSuccess = create_results(
            [
                Result(
                    part_number=unique_identifier,
                    keywords=[original_keyword],
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = create_response.results[0]
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
        self, client: ResultClient, create_results, unique_identifier
    ):
        original_keyword = "originalKeyword"
        additional_keyword = "additionalKeyword"
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        create_response: ResultsPartialSuccess = create_results(
            [
                Result(
                    part_number=unique_identifier,
                    keywords=[original_keyword],
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = create_response.results[0]
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
        self, client: ResultClient, create_results, unique_identifier
    ):
        new_key = "newKey"
        original_properties = {"originalKey": "originalValue"}
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        new_properties = {new_key: "newValue"}
        create_response: ResultsPartialSuccess = create_results(
            [
                Result(
                    part_number=unique_identifier,
                    properties=original_properties,
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = create_response.results[0]
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
        self, client: ResultClient, create_results, unique_identifier
    ):
        original_key = "originalKey"
        new_key = "newKey"
        original_properties = {original_key: "originalValue"}
        program_name = "Test Program"
        status = StatusObject(status_type=StatusType.PASSED, status_name="Passed")
        new_properties = {new_key: "newValue"}
        create_response: ResultsPartialSuccess = create_results(
            [
                Result(
                    part_number=unique_identifier,
                    properties=original_properties,
                    program_name=program_name,
                    status=status,
                )
            ]
        )
        assert create_response is not None
        assert len(create_response.results) == 1

        updated_result = create_response.results[0]
        updated_result.properties = new_properties
        update_response = client.update_results([updated_result], replace=False)

        assert update_response is not None
        assert len(update_response.results) == 1
        updated_result = update_response.results[0]
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
