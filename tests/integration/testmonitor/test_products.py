from typing import List
import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateProductsPartialSuccess,
    Product,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestMonitorClient:
    """Fixture to create a TestMonitorClient instance."""
    return TestMonitorClient(enterprise_config)


@pytest.fixture
def create_products(client: TestMonitorClient):
    """Fixture to return a factory that creates specs."""
    responses: List[CreateProductsPartialSuccess] = []

    def _create_products(products: List[Product]) -> CreateProductsPartialSuccess:
        response = client.create_products(products)
        responses.append(response)
        return response

    yield _create_products

    created_products: List[Product] = []
    for response in responses:
        if response.products:
            created_products = created_products + response.products
    client.delete_products(ids=[product.id for product in created_products])


@pytest.mark.integration
@pytest.mark.enterprise
class TestTestMonitor:
    def test__api_info__returns(self, client: TestMonitorClient):
        response = client.api_info()
        assert len(response.dict()) != 0

    def test__create_single_product__one_product_created_with_right_field_values(
        self, client: TestMonitorClient, create_products
    ):
        part_number = "Example 123 AA"
        name = "Test Name"
        family = "Example Family"
        keywords = ["testing"]
        properties = {"test_property": "yes"}
        product = Product(
            part_number=part_number,
            name=name,
            family=family,
            keywords=keywords,
            properties=properties,
        )

        response: CreateProductsPartialSuccess = create_products([product])
        assert response is not None
        assert len(response.products) == 1
        created_product = response.products[0]
        assert created_product.part_number == part_number
        assert created_product.name == name
        assert created_product.family == family
        assert created_product.keywords == keywords
        assert created_product.properties == properties
