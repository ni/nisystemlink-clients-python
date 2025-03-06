from datetime import datetime
from typing import List

import pandas as pd
import pytest
from nisystemlink.clients.product.models import Product
from nisystemlink.clients.product.utilities import convert_products_to_dataframe
from pandas import DataFrame


@pytest.fixture
def mock_products_data() -> List[Product]:
    """Fixture to return a mock product data."""
    product1 = Product(
        id="5ffb2bf6771fa11e877838dd1",
        part_number="p1",
        name="product_1",
        family="product_family",
        updated_at=datetime(2024, 2, 2, 14, 22, 4, 625155),
        file_ids=["file11", "file12"],
        keywords=["keyword11", "keyword12"],
        properties={"property11": "property11_value", "property12": "property12_value"},
        workspace="5ffb2bf6771fa11e877838dd0",
    )
    product2 = Product(
        id="5ffb2bf6771fa11e877838dd2",
        part_number="p2",
        name="product_2",
        family="product_family",
        updated_at=datetime(2024, 2, 2, 14, 22, 4, 625455),
        file_ids=["file21", "file22"],
        keywords=["keyword21", "keyword22"],
        properties={"property21": "property21_value"},
        workspace="5ffb2bf6771fa11e877838dd0",
    )

    return [product1, product2]


@pytest.fixture
def expected_products_dataframe(mock_products_data: List[Product]) -> DataFrame:
    """Fixture to return the expected DataFrame based on the mock product data."""
    return pd.json_normalize(
        [mock_product.dict() for mock_product in mock_products_data]
    )


@pytest.fixture
def empty_products_data() -> List:
    """Fixture to return an empty list of products."""
    return []


@pytest.mark.enterprise
@pytest.mark.unit
class TestProductDataframeUtilities:
    def test__convert_products_to_dataframe__with_complete_data(
        self, mock_products_data: List[Product], expected_products_dataframe: DataFrame
    ):
        """Test normal case with valid product data."""
        products_dataframe = convert_products_to_dataframe(mock_products_data)

        assert not products_dataframe.empty
        assert (
            products_dataframe.columns.to_list()
            == expected_products_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            products_dataframe, expected_products_dataframe, check_dtype=True
        )

    def test__convert_products_to_dataframe__with_empty_data(
        self, empty_products_data: List
    ):
        """Test case when the input products data is empty."""
        products_dataframe = convert_products_to_dataframe(empty_products_data)

        assert products_dataframe.empty

    def test__convert_products_to_dataframe__with_missing_fields(
        self, mock_products_data: List[Product], expected_products_dataframe: DataFrame
    ):
        """Test case when some fields in product data are missing."""
        products = mock_products_data
        for product in products:
            product.keywords = None
            product.properties = None

        products_dataframe = convert_products_to_dataframe(products)
        expected_products_dataframe = expected_products_dataframe.drop(
            columns=expected_products_dataframe.filter(
                like="properties"
            ).columns.to_list()
            + ["keywords"]
        )

        assert not products_dataframe.empty
        assert (
            products_dataframe.columns.to_list()
            == expected_products_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            products_dataframe, expected_products_dataframe, check_dtype=True
        )
