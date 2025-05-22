from typing import List

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.systems._systems_client import SystemsClient
from nisystemlink.clients.systems.models._create_virtual_systems_request import (
    CreateVirtualSystemRequest,
)
from nisystemlink.clients.systems.models._create_virtual_systems_response import (
    CreateVirtualSystemResponse,
)
from nisystemlink.clients.systems.models._query_systems_request import (
    QuerySystemsRequest,
)
from nisystemlink.clients.systems.models._query_systems_response import (
    QuerySystemsResponse,
)
from nisystemlink.clients.systems.models._remove_systems_request import (
    RemoveSystemsRequest,
)
from nisystemlink.clients.systems.models._remove_systems_response import (
    RemoveSystemsResponse,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> SystemsClient:
    """Fixture to create a TestPlanTemplateClient instance."""
    return SystemsClient(enterprise_config)


@pytest.fixture
def create_virtual_systems(client: SystemsClient):
    """Fixture to return a factory that create test plan templates."""
    responses: List[CreateVirtualSystemResponse] = []

    def _create_virtual_systems(
        new_virtual_systems: CreateVirtualSystemRequest,
    ) -> CreateVirtualSystemResponse:
        response = client.create_virtual_system(
            create_virtual_system_request=new_virtual_systems
        )
        responses.append(response)
        return response

    yield _create_virtual_systems

    created_virtual_systems_minion_ids: List[str] = []
    for response in responses:
        if response.minionId:
            created_virtual_systems_minion_ids = created_virtual_systems_minion_ids + [
                response.minionId
            ]
        client.remove_systems(
            virtual_system_to_remove=RemoveSystemsRequest(
                tgt=created_virtual_systems_minion_ids,
            )
        )


@pytest.mark.integration
@pytest.mark.enterprise
class TestSystemsClient:
    def test__create_virtual_systems__returns_created_virtual_system(
        self, client: SystemsClient, create_virtual_systems
    ):
        create_virtual_system_request: CreateVirtualSystemRequest = (
            CreateVirtualSystemRequest(
                alias="Python integration virtual system",
                workspace="33eba2fe-fe42-48a1-a47f-a6669479a8aa",
            )
        )

        create_virtual_system_response = create_virtual_systems(
            create_virtual_system_request
        )

        minion_id = (
            create_virtual_system_response.minionId
            if create_virtual_system_response
            and create_virtual_system_response.minionId
            else None
        )

        assert minion_id is not None

    def test__query_systems__returns_queried_virtual_system(
        self, client: SystemsClient, create_virtual_systems
    ):
        create_virtual_system_request: CreateVirtualSystemRequest = (
            CreateVirtualSystemRequest(
                alias="Python integration virtual system",
                workspace="33eba2fe-fe42-48a1-a47f-a6669479a8aa",
            )
        )

        create_virtual_system_response = create_virtual_systems(
            create_virtual_system_request
        )

        minion_id = (
            create_virtual_system_response.minionId
            if create_virtual_system_response
            and create_virtual_system_response.minionId
            else None
        )

        assert minion_id is not None

        query_virtual_system_response: QuerySystemsResponse = client.query_systems(
            query=QuerySystemsRequest(filter=f'id="{minion_id}"')
        )

        assert query_virtual_system_response.data is not None
        assert query_virtual_system_response.data[0].id == minion_id

    def test__remove_sytems(self, client: SystemsClient):

        create_virtual_system_request: CreateVirtualSystemRequest = (
            CreateVirtualSystemRequest(
                alias="Python integration query virtual system",
                workspace="33eba2fe-fe42-48a1-a47f-a6669479a8aa",
            )
        )

        create_virtual_system_response: CreateVirtualSystemResponse = (
            client.create_virtual_system(
                create_virtual_system_request=create_virtual_system_request
            )
        )

        minion_id = (
            create_virtual_system_response.minionId
            if create_virtual_system_response
            and create_virtual_system_response.minionId
            else None
        )

        assert minion_id is not None

        remove_system_response: RemoveSystemsResponse = client.remove_systems(
            virtual_system_to_remove=RemoveSystemsRequest(tgt=[minion_id])
        )

        assert remove_system_response.removed_ids is not None
        assert remove_system_response.removed_ids[0] == minion_id
