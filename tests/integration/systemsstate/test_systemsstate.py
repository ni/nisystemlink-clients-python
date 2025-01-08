from typing import List

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.systemsstate import models
from nisystemlink.clients.systemsstate import SystemsStateClient


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> SystemsStateClient:
    """Fixture to create a SystemsStateClient instance."""
    return SystemsStateClient(enterprise_config)


@pytest.fixture
def default_work_space() -> str:
    """Fixture that returns the default workspace id"""
    return "846e294a-a007-47ac-9fc2-fac07eab240e"


@pytest.fixture
def create_state(client: SystemsStateClient):
    """Fixture to return a factory function for creating states.

    This fixture:
    - Provides a helper function to create states using the provided client.
    - Tracks created states and ensures they are deleted after the test.

    Cleanup:
    - Deletes all states created during the test, if any.
    """
    states_created: List[models.StateResponse] = []

    def _create_state_helper(new_state: models.StateRequest) -> models.StateResponse:
        response = client.create_state(new_state)
        states_created.append(response)
        return response

    yield _create_state_helper

    states_id_list = [state.id for state in states_created if state.id is not None]
    print(f"States id list: {states_id_list}")
    if states_id_list:
        print(f"Cleaning up states: {states_id_list}")
        client.delete_states(states_id_list)


@pytest.mark.integration
@pytest.mark.enterprise
class TestSystemsState:
    def test__create_single_state__state_created_with_right_field_values(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        name = "Test State"
        description = "Test Description"
        properties = {"test_property": "test_value"}
        system_image = {"name": "System Image Name", "version": "1.0"}
        state = models.StateRequest(
            name=name,
            description=description,
            properties=properties,
            workspace=default_work_space,
            architecture=models.Architecture.X64,
            distribution=models.Distribution.ANY,
            systemImage=system_image,
        )

        response = create_state(state)

        assert response is not None
        assert response.name == name
        assert response.description == description
        assert response.properties == properties
        assert response.workspace == default_work_space

    def test__create_multiple_states__multiple_creates_succeed(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        states = [
            models.StateRequest(
                name=f"Test State {i}",
                workspace=default_work_space,
                architecture=models.Architecture.X64,
                distribution=models.Distribution.ANY,
                systemImage={"name": "System Image Name", "version": "1.0"},
            )
            for i in range(2)
        ]

        responses = [create_state(state) for state in states]

        assert all(response is not None for response in responses)
        assert len(responses) == 2

    def test__create_single_state_and_get_states__at_least_one_state_exists(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        state = models.StateRequest(
            name="Test Get States",
            workspace=default_work_space,
            architecture=models.Architecture.X64,
            distribution=models.Distribution.ANY,
            systemImage={"name": "System Image Name", "version": "1.0"},
        )
        create_state(state)

        get_response = client.get_states(workspace=default_work_space)

        assert get_response is not None
        assert get_response.states is not None
        assert len(get_response.states) >= 1

    def test__create_multiple_states_and_get_states_with_take__only_take_returned(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        states = [
            models.StateRequest(
                name=f"Test State Take {i}",
                workspace=default_work_space,
                architecture=models.Architecture.X64,
                distribution=models.Distribution.ANY,
                systemImage={"name": "System Image Name", "version": "1.0"},
            )
            for i in range(2)
        ]
        for state in states:
            create_state(state)

        get_response = client.get_states(take=1, workspace=default_work_space)

        assert get_response is not None
        assert get_response.states is not None
        assert len(get_response.states) == 1

    def test__get_state_by_id__state_matches_expected(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        name = "Test Get By ID"
        state = models.StateRequest(
            name=name,
            workspace=default_work_space,
            architecture=models.Architecture.X64,
            distribution=models.Distribution.ANY,
            systemImage={"name": "System Image Name", "version": "1.0"},
        )
        created_state = create_state(state)
        assert created_state is not None

        retrieved_state = client.get_state(created_state.id)

        assert retrieved_state is not None
        assert retrieved_state.name == name

    def test__update_state_properties__properties_updated(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        original_properties = {"original_key": "original_value"}
        new_properties = {"new_key": "new_value"}

        state = models.StateRequest(
            name="Test Update Properties",
            workspace=default_work_space,
            properties=original_properties,
            architecture=models.Architecture.X64,
            distribution=models.Distribution.ANY,
            systemImage={"name": "System Image Name", "version": "1.0"},
        )
        created_state = create_state(state)
        assert created_state is not None

        update_response = client.update_state(created_state.id, new_properties)

        assert update_response is not None
        assert update_response.properties == new_properties

    def test__replace_state_content__content_replaced(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        state = models.StateRequest(
            name="Test Replace Content",
            workspace=default_work_space,
            architecture=models.Architecture.X64,
            distribution=models.Distribution.ANY,
            systemImage={"name": "System Image Name", "version": "1.0"},
        )
        created_state = create_state(state)
        assert created_state is not None

        test_content = "Test content"
        change_description = "Test change"

        updated_state = client.replace_state_content(
            created_state.id, change_description, test_content
        )

        assert updated_state is not None
        assert updated_state.id == created_state.id
        assert updated_state.description == change_description

    def test__export_state__state_exported(
        self, client: SystemsStateClient, create_state, default_work_space
    ):
        state = models.StateRequest(
            name="Test Export",
            workspace=default_work_space,
            architecture=models.Architecture.X64,
            distribution=models.Distribution.ANY,
            systemImage={"name": "System Image Name", "version": "1.0"},
        )
        created_state = create_state(state)
        assert created_state is not None

        export_request = models.ExportStateRequest(
            state={
                "stateID": created_state.id,
            }
        )
        exported_content = client.export_state(export_request)

        assert exported_content is not None

    def test__import_state__state_imported(
        self, client: SystemsStateClient, default_work_space
    ):
        name = "Test Import"
        description = "Test Import Description"
        test_file = "Test state file content"
        properties = "{}"  # Empty JSON string for properties

        imported_state = client.import_state(
            name=name,
            description=description,
            distribution=models.Distribution.ANY.value,
            architecture=models.Architecture.X64.value,
            properties=properties,
            workspace=default_work_space,
            file=test_file,
        )

        assert imported_state is not None
        assert imported_state.name == name
        assert imported_state.description == description
