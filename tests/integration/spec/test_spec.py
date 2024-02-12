import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.spec.models import (
    CreateSpecificationRequestObject,
    CreateSpecificationsRequest,
    Type,
)
from nisystemlink.clients.spec import SpecClient


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
