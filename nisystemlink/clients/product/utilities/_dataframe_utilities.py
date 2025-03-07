from typing import List

import pandas as pd
from nisystemlink.clients.product.models import Product
from pandas import DataFrame


def convert_products_to_dataframe(products: List[Product]) -> DataFrame:
    """Converts a list of products into a normalized dataframe.

    Args:
        products (List[Product]): A list of products

    Returns:
        DataFrame:
            - A Pandas DataFrame containing the product data. The DataFrame would consist of all the
            fields in the input products.
            - A new column would be created for unique properties across all products. The property
            columns would be named in the format `properties.property_name`.
    """
    products_dict_representation = [
        product.dict(exclude_none=True) for product in products
    ]
    normalized_products_dataframe = pd.json_normalize(
        products_dict_representation, sep="."
    )

    return normalized_products_dataframe
