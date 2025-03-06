from typing import List

import pandas as pd
from nisystemlink.clients.product.models import Product
from pandas import DataFrame


def convert_products_to_dataframe(products: List[Product]) -> DataFrame:
    """Converts a list of products into a normalized dataframe.

    Args:
        products (List[Product]): A list of product responses retrieved from the API.

    Returns:
        DataFrame:
            - A Pandas DataFrame containing the normalized product data. The DataFrame would consist
            of all the fields received from the product response.

            - Further, the properties field alone would get normalized. In the sense, there
            would be separate columns for each of the properties in the list of all products. The
            normalized column headers would be in the format `properties.property_name`.
    """
    products_dict_representation = [product.dict() for product in products]
    normalized_products_dataframe = pd.json_normalize(
        products_dict_representation, sep="."
    )
    normalized_products_dataframe.dropna(axis="columns", how="all", inplace=True)

    return normalized_products_dataframe
