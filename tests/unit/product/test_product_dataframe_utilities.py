from datetime import datetime
from typing import List

import pandas as pd
import pytest
from nisystemlink.clients.product.models import Product
from nisystemlink.clients.product.utilities import convert_products_to_dataframe
from pandas import DataFrame


@pytest.fixture
def mock_product_data() -> List[Product]:
    """Fixture to return a mock product data."""
    product = Product(
        id="product_id",
        part_number="product_part_number",
        name="product_name",
        family="product_family",
        updated_at=datetime(2024, 2, 2, 14, 22, 4, 625155),
        file_ids=["file1", "file2"],
        keywords=["keyword1", "keyword2"],
        properties={"property1": "property1_value", "property2": "property2_value"},
        workspace="product_workspace",
    )

    return [product]


@pytest.fixture
def expected_products_dataframe(mock_product_data) -> DataFrame:
    """Fixture to return the expected DataFrame based on the mock product data."""
    product = mock_product_data[0]
    expected_dataframe_structure = {
        "id": product.id,
        "part_number": product.part_number,
        "name": product.name,
        "family": product.family,
        "updated_at": product.updated_at,
        "file_ids": product.file_ids,
        "keywords": product.keywords,
        "workspace": product.workspace,
        "properties.property1": "property1_value",
        "properties.property2": "property2_value",
    }

    return pd.json_normalize(expected_dataframe_structure)


@pytest.fixture
def empty_products_data() -> List:
    """Fixture to return an empty list of products."""
    return []


@pytest.mark.enterprise
@pytest.mark.unit
class TestProductDataframeUtilities:
    def test__convert_products_to_dataframe__with_complete_data(
        self, mock_product_data, expected_products_dataframe
    ):
        """Test normal case with valid product data."""
        products_dataframe = convert_products_to_dataframe(mock_product_data)

        assert not products_dataframe.empty
        assert (
            products_dataframe.columns.to_list()
            == expected_products_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            products_dataframe, expected_products_dataframe, check_dtype=True
        )

    def test__convert_products_to_dataframe__with_empty_data(self, empty_products_data):
        """Test case when the input products data is empty."""
        products_dataframe = convert_products_to_dataframe(empty_products_data)

        assert products_dataframe.empty

    def test__convert_products_to_dataframe__with_missing_fields(
        self, mock_product_data, expected_products_dataframe
    ):
        """Test case when some fields in product data are missing."""
        products = mock_product_data
        products[0].keywords = None
        products[0].properties = None

        products_dataframe = convert_products_to_dataframe(products)
        expected_products_dataframe = expected_products_dataframe.drop(
            columns=["keywords", "properties.property1", "properties.property2"]
        )

        assert not products_dataframe.empty
        assert (
            products_dataframe.columns.to_list()
            == expected_products_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            products_dataframe, expected_products_dataframe, check_dtype=True
        )
