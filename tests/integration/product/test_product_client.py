import uuid
from typing import List

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.product._product_client import ProductClient
from nisystemlink.clients.product.models import (
    CreateProductsPartialSuccess,
    Product,
)
from nisystemlink.clients.product.models._paged_products import PagedProducts
from nisystemlink.clients.product.models._query_products_request import (
    ProductField,
    QueryProductsRequest,
    QueryProductValuesRequest,
)
from nisystemlink.clients.product.utilities import get_products_linked_to_file


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> ProductClient:
    """Fixture to create a ProductClient instance."""
    return ProductClient(enterprise_config)


@pytest.fixture
def unique_identifier() -> str:
    """Unique product id for this test."""
    product_id = uuid.uuid1().hex
    return product_id


@pytest.fixture
def create_products(client: ProductClient):
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
    client.delete_products(ids=[str(product.id) for product in created_products])


@pytest.mark.integration
@pytest.mark.enterprise
class TestProductClient:

    def test__create_single_product__one_product_created_with_right_field_values(
        self, client: ProductClient, create_products, unique_identifier
    ):
        part_number = unique_identifier
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

    def test__create_multiple_products__multiple_creates_succeed(
        self, client: ProductClient, create_products
    ):
        products = [
            Product(part_number=uuid.uuid1().hex),
            Product(part_number=uuid.uuid1().hex),
        ]
        response: CreateProductsPartialSuccess = create_products(products)
        assert response is not None
        assert len(response.products) == 2

    def test__create_single_product_and_get_products__at_least_one_product_exists(
        self, client: ProductClient, create_products, unique_identifier
    ):
        products = [Product(part_number=unique_identifier)]
        create_products(products)
        get_response = client.get_products()
        assert get_response is not None
        assert len(get_response.products) >= 1

    def test__create_multiple_products_and_get_products_with_take__only_take_returned(
        self, client: ProductClient, create_products, unique_identifier
    ):
        products = [
            Product(part_number=unique_identifier),
            Product(part_number=unique_identifier),
        ]
        create_products(products)
        get_response = client.get_products(take=1)
        assert get_response is not None
        assert len(get_response.products) == 1

    def test__create_multiple_products_and_get_products_with_count_at_least_one_count(
        self, client: ProductClient, create_products, unique_identifier
    ):
        products = [
            Product(part_number=unique_identifier),
            Product(part_number=unique_identifier),
        ]
        create_products(products)
        get_response: PagedProducts = client.get_products(return_count=True)
        assert get_response is not None
        assert get_response.total_count is not None and get_response.total_count >= 2

    def test__get_product_by_id__product_matches_expected(
        self, client: ProductClient, create_products, unique_identifier
    ):
        part_number = unique_identifier
        products = [Product(part_number=part_number)]
        create_response: CreateProductsPartialSuccess = create_products(products)
        assert create_response is not None
        id = str(create_response.products[0].id)
        product = client.get_product(id)
        assert product is not None
        assert product.part_number == part_number

    def test__query_product_by_part_number__matches_expected(
        self, client: ProductClient, create_products, unique_identifier
    ):
        part_number = unique_identifier
        products = [Product(part_number=part_number)]
        create_response: CreateProductsPartialSuccess = create_products(products)
        assert create_response is not None
        query_request = QueryProductsRequest(
            filter=f'partNumber="{part_number}"', return_count=True
        )
        query_response: PagedProducts = client.query_products(query_request)
        assert query_response.total_count == 1
        assert query_response.products[0].part_number == part_number

    def test__query_product_values_for_name__name_matches(
        self, client: ProductClient, create_products, unique_identifier
    ):
        part_number = unique_identifier
        test_name = "query values test"
        create_response: CreateProductsPartialSuccess = create_products(
            [Product(part_number=part_number, name=test_name)]
        )
        assert create_response is not None
        query_request = QueryProductValuesRequest(
            filter=f'partNumber="{part_number}"', field=ProductField.NAME
        )
        query_response: List[str] = client.query_product_values(query_request)
        assert query_response is not None
        assert len(query_response) == 1
        assert query_response[0] == test_name

    def test__update_keywords_with_replace__keywords_replaced(
        self, client: ProductClient, create_products, unique_identifier
    ):
        original_keyword = "originalKeyword"
        updated_keyword = "updatedKeyword"
        create_response: CreateProductsPartialSuccess = create_products(
            [Product(part_number=unique_identifier, keywords=[original_keyword])]
        )
        assert create_response is not None
        assert len(create_response.products) == 1
        updated_product = create_response.products[0]
        updated_product.keywords = [updated_keyword]
        update_response = client.update_products([updated_product], replace=True)
        assert update_response is not None
        assert len(update_response.products) == 1
        assert (
            update_response.products[0].keywords is not None
            and updated_keyword in update_response.products[0].keywords
        )
        assert original_keyword not in update_response.products[0].keywords

    def test__update_keywords_no_replace__keywords_appended(
        self, client: ProductClient, create_products, unique_identifier
    ):
        original_keyword = "originalKeyword"
        additional_keyword = "additionalKeyword"
        create_response: CreateProductsPartialSuccess = create_products(
            [Product(part_number=unique_identifier, keywords=[original_keyword])]
        )
        assert create_response is not None
        assert len(create_response.products) == 1
        updated_product = create_response.products[0]
        updated_product.keywords = [additional_keyword]
        update_response = client.update_products([updated_product], replace=False)
        assert update_response is not None
        assert len(update_response.products) == 1
        assert (
            update_response.products[0].keywords is not None
            and original_keyword in update_response.products[0].keywords
        )
        assert (
            update_response.products[0].keywords is not None
            and additional_keyword in update_response.products[0].keywords
        )

    def test__update_properties_with_replace__properties_replaced(
        self, client: ProductClient, create_products, unique_identifier
    ):
        new_key = "newKey"
        original_properties = {"originalKey": "originalValue"}
        new_properties = {new_key: "newValue"}
        create_response: CreateProductsPartialSuccess = create_products(
            [Product(part_number=unique_identifier, properties=original_properties)]
        )
        assert create_response is not None
        assert len(create_response.products) == 1
        updated_product = create_response.products[0]
        updated_product.properties = new_properties
        update_response = client.update_products([updated_product], replace=True)
        assert update_response is not None
        assert len(update_response.products) == 1
        assert (
            update_response.products[0].properties is not None
            and len(update_response.products[0].properties) == 1
        )
        assert new_key in update_response.products[0].properties.keys()
        assert (
            update_response.products[0].properties[new_key] == new_properties[new_key]
        )

    def test__update_properties_append__properties_appended(
        self, client: ProductClient, create_products, unique_identifier
    ):
        original_key = "originalKey"
        new_key = "newKey"
        original_properties = {original_key: "originalValue"}
        new_properties = {new_key: "newValue"}
        create_response: CreateProductsPartialSuccess = create_products(
            [Product(part_number=unique_identifier, properties=original_properties)]
        )
        assert create_response is not None
        assert len(create_response.products) == 1
        updated_product = create_response.products[0]
        updated_product.properties = new_properties
        update_response = client.update_products([updated_product], replace=False)
        assert update_response is not None
        assert len(update_response.products) == 1
        updated_product = update_response.products[0]
        assert (
            updated_product.properties is not None
            and len(updated_product.properties) == 2
        )
        assert original_key in updated_product.properties.keys()
        assert new_key in updated_product.properties.keys()
        assert (
            updated_product.properties[original_key]
            == original_properties[original_key]
        )
        assert updated_product.properties[new_key] == new_properties[new_key]

    def test__query_products_linked_to_files_correct_products_returned(
        self, client: ProductClient, create_products
    ):
        file_id = uuid.uuid1().hex
        product_name_with_file = "Has File"
        products = [
            Product(
                part_number=uuid.uuid1().hex,
                name=product_name_with_file,
                file_ids=[file_id],
            ),
            Product(part_number=uuid.uuid1().hex, name="No File Link"),
        ]
        print(products)
        create_response: CreateProductsPartialSuccess = create_products(products)
        assert create_response is not None
        assert len(create_response.products) == 2
        linked_products = get_products_linked_to_file(client, file_id)
        names = [product.name for product in linked_products]
        assert product_name_with_file in names
