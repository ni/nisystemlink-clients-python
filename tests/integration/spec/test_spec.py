import pytest

from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    CreateSpecificationRequestObject,
    CreateSpecificationsRequest,
    DeleteSpecificationsRequest,
    Type,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> SpecClient:
    """Fixture ot create a SpecClient instance."""
    return SpecClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestSpec:
    def test__api_info__returns(self, client: SpecClient):
        response = client.api_info()
        assert len(response.dict()) != 0

    def test__create_single_spec__one_created_with_right_field_values(
        self, client: SpecClient
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
        response = client.create_specs(CreateSpecificationsRequest(specs=[spec]))
        assert response is not None
        assert len(response.created_specs) == 1
        created_spec = response.created_specs[0]
        assert created_spec.product_id == productId
        assert created_spec.spec_id == specId

        delete_response = client.delete_specs(
            DeleteSpecificationsRequest(ids=[created_spec.id])
        )
        assert delete_response is None

    def test__create_multiple_specs__all_succeed(self, client: SpecClient):
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
        response = client.create_specs(CreateSpecificationsRequest(specs=specs))
        assert response is not None
        assert len(response.created_specs) == 2

        delete_response = client.delete_specs(
            DeleteSpecificationsRequest(
                ids=[spec.id for spec in response.created_specs]
            )
        )
        assert delete_response is None

    def test__create_duplicate_spec__errors(self, client: SpecClient):
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
        response = client.create_specs(CreateSpecificationsRequest(specs=[spec]))
        assert response is not None
        assert len(response.created_specs) == 1

        fail_response = client.create_specs(CreateSpecificationsRequest(specs=[spec]))
        assert len(fail_response.failed_specs) == 1
        assert len(fail_response.created_specs) == 0
        assert fail_response.failed_specs[0].spec_id == duplicate_id

        delete_response = client.delete_specs(
            DeleteSpecificationsRequest(ids=[response.created_specs[0].id])
        )
        assert delete_response is None
