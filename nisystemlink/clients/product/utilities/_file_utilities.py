from typing import List

from nisystemlink.clients.product._product_client import ProductClient
from nisystemlink.clients.product.models._paged_products import PagedProducts
from nisystemlink.clients.product.models._product import (
    Product,
)
from nisystemlink.clients.product.models._query_products_request import (
    QueryProductsRequest,
)


def get_products_linked_to_file(client: ProductClient, file_id: str) -> List[Product]:
    """Gets a list of all the products that are linked to the file.

    Args:
        `client` : The `ProductClient` to use for the request.
        `file_id`: The id of the file to query links for.

    Returns:
        `List[Product]`: A list of all the products that are linked to the file with `file_id`
    """
    query_request = QueryProductsRequest(
        filter=f'fileIds.Contains("{file_id}")', take=100
    )
    response: PagedProducts = client.query_products_paged(query_request)
    products = response.products
    while response.continuation_token:
        query_request.continuation_token = response.continuation_token
        response = client.query_products_paged(query_request)
        products.extend(response.products)
    return products
