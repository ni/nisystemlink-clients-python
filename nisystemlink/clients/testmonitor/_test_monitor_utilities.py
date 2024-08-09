from typing import List

from nisystemlink.clients.testmonitor._test_monitor_client import TestMonitorClient
from nisystemlink.clients.testmonitor.models._paged_products import PagedProducts
from nisystemlink.clients.testmonitor.models._product import Product
from nisystemlink.clients.testmonitor.models._query_products_request import (
    QueryProductsRequest,
)


def get_products_linked_to_file(
    client: TestMonitorClient, file_id: str
) -> List[Product]:
    """Gets a list of all the products that are linked to the file.

    Args:
        `client` : The `TestMonitorClient` to use for the request.
        `file_id`: The id of the file to query links for.

    Returns:
        A list of all the products that are linked to the file with `file_id`
    """
    query_request = QueryProductsRequest(
        filter=f'fileIds.Contains("{file_id}")', take=100
    )
    response: PagedProducts = client.query_products(query_request)
    products = response.products
    while response.continuation_token:
        query_request.continuation_token = response.continuation_token
        response = client.query_products(query_request)
        products.extend(response.products)
    return products
