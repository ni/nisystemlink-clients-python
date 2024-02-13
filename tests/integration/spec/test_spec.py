from typing import List, Optional

import pytest

from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    CreateSpecificationRequestObject,
    CreateSpecificationsPartialSuccessResponse,
    CreateSpecificationsRequest,
    DeleteSpecificationsRequest,
    QuerySpecificationsRequest,
    Type,
    UpdateSpecificationRequestObject,
    UpdateSpecificationsRequest,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> SpecClient:
    """Fixture ot create a SpecClient instance."""
    return SpecClient(enterprise_config)


@pytest.fixture
def create_specs(client: SpecClient):
    """Fixture to return a factory that creates specs."""
    responses: List[CreateSpecificationsPartialSuccessResponse] = []

    def _create_specs(new_specs: Optional[CreateSpecificationsRequest]) -> str:
        response = client.create_specs(new_specs)
        responses.append(response)
        return response

    yield _create_specs

    created_specs = []
    for response in responses:
        created_specs = created_specs + response.created_specs
    client.delete_specs(
        DeleteSpecificationsRequest(ids=[spec.id for spec in created_specs])
    )


@pytest.fixture
def create_specs_for_query(create_specs):
    """Fixture for creating a set of specs that can be used to test query operations."""
    product = "TestProduct"
    spec_documents = [
        {
            "specId": "spec1",
            "name": "output voltage",
            "type": Type.FUNCTIONAL,
            "category": "ParametricSpecs",
        },
        {
            "specId": "spec2",
            "name": "noise",
            "type": Type.FUNCTIONAL,
            "category": "Noise Thresholds",
        },
        {
            "specId": "spec3",
            "name": "input voltage",
            "type": Type.FUNCTIONAL,
            "category": "ParametricSpecs",
        },
    ]
    spec_requests = []
    for spec in spec_documents:
        new_spec = CreateSpecificationRequestObject(
            product_id=product,
            spec_id=spec["specId"],
            type=spec["type"],
            category=spec["category"],
            name=spec["name"],
        )
        spec_requests.append(new_spec)
    return create_specs(CreateSpecificationsRequest(specs=spec_requests))


@pytest.mark.integration
@pytest.mark.enterprise
class TestSpec:
    def test__api_info__returns(self, client: SpecClient):
        response = client.api_info()
        assert len(response.dict()) != 0

    def test__create_single_spec__one_created_with_right_field_values(
        self, client: SpecClient, create_specs
    ):
        specId = "spec1"
        productId = "TestProduct"
        spec = CreateSpecificationRequestObject(
            productId=productId,
            specId=specId,
            type=Type.FUNCTIONAL,
            keywords=["work", "reviewed"],
            category="Parametric Specs",
            block="newBlock",
        )
        response = create_specs(CreateSpecificationsRequest(specs=[spec]))
        assert response is not None
        assert len(response.created_specs) == 1
        created_spec = response.created_specs[0]
        assert created_spec.product_id == productId
        assert created_spec.spec_id == specId

    def test__create_multiple_specs__all_succeed(
        self, client: SpecClient, create_specs
    ):
        specIds = ["spec1", "spec2"]
        productId = "TestProduct"
        specs = []
        for id in specIds:
            spec = CreateSpecificationRequestObject(
                productId=productId,
                specId=id,
                type=Type.FUNCTIONAL,
                keywords=["work", "reviewed"],
                category="Parametric Specs",
                block="newBlock",
            )
            specs.append(spec)
        response = create_specs(CreateSpecificationsRequest(specs=specs))
        assert response is not None
        assert len(response.created_specs) == 2

    def test__create_duplicate_spec__errors(self, client: SpecClient, create_specs):
        duplicate_id = "spec1"
        productId = "TestProduct"
        spec = CreateSpecificationRequestObject(
            productId=productId,
            specId=duplicate_id,
            type=Type.FUNCTIONAL,
            keywords=["work", "reviewed"],
            category="Parametric Specs",
            block="newBlock",
        )
        response = create_specs(CreateSpecificationsRequest(specs=[spec]))
        assert response is not None
        assert len(response.created_specs) == 1

        fail_response = create_specs(CreateSpecificationsRequest(specs=[spec]))
        assert len(fail_response.failed_specs) == 1
        assert len(fail_response.created_specs) == 0
        assert fail_response.failed_specs[0].spec_id == duplicate_id

    def test__delete_existing_spec__succeeds(self, client: SpecClient):
        # Not using the fixture here so that we can inspect delete response.
        specId = "spec1"
        productId = "TestProduct"
        spec = CreateSpecificationRequestObject(
            productId=productId,
            specId=specId,
            type=Type.FUNCTIONAL,
        )
        response = client.create_specs(CreateSpecificationsRequest(specs=[spec]))
        created_spec = response.created_specs[0]

        delete_response = client.delete_specs(
            DeleteSpecificationsRequest(ids=[created_spec.id])
        )
        assert delete_response is None

    def test__delete_non_existant_spec__delete_fails(self, client: SpecClient):
        bad_id = "DEADBEEF"
        delete_response = client.delete_specs(DeleteSpecificationsRequest(ids=[bad_id]))
        assert bad_id in delete_response.failed_spec_ids

    def test__update_single_same_version__version_updates(
        self, client: SpecClient, create_specs
    ):
        spec = CreateSpecificationRequestObject(
            productId="TestProduct",
            specId="spec1",
            type=Type.FUNCTIONAL,
            keywords=["work", "reviewed"],
            category="Parametric Specs",
            block="newBlock",
        )
        response = create_specs(CreateSpecificationsRequest(specs=[spec]))
        assert response is not None
        assert len(response.created_specs) == 1
        created_spec = response.created_specs[0]
        assert created_spec.version == 0

        update_spec = UpdateSpecificationRequestObject(
            id=created_spec.id,
            product_id=created_spec.product_id,
            spec_id=created_spec.spec_id,
            type=Type.FUNCTIONAL,
            keywords=["work", "reveiwed"],
            block="modifiedBlock",
            version=created_spec.version,
            workspace=created_spec.workspace,
        )

        update_response = client.update_specs(
            specs=UpdateSpecificationsRequest(specs=[update_spec])
        )
        assert update_response is not None
        assert len(update_response.updated_specs) == 1
        updated_spec = update_response.updated_specs[0]
        assert updated_spec.version == 1

    def test__query_product__all_returned(
        self, client: SpecClient, create_specs, create_specs_for_query
    ):
        request = QuerySpecificationsRequest(productIds=["TestProduct"])

        response = client.query_specs(request)
        assert len(response.specs) == 3

    def test__query_spec_name__two_returned(
        self, client: SpecClient, create_specs, create_specs_for_query
    ):
        request = QuerySpecificationsRequest(
            product_ids=["TestProduct"], filter='name.Contains("voltage")'
        )
        response = client.query_specs(request)
        assert len(response.specs) == 2

    def test__query_spec_category_one_returned(
        self, client: SpecClient, create_specs, create_specs_for_query
    ):
        request = QuerySpecificationsRequest(
            product_ids=["TestProduct"], filter='category == "Noise Thresholds"'
        )
        response = client.query_specs(request)
        assert len(response.specs) == 1
