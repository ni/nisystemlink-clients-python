"""Implementation of TestMonitor Client"""

from typing import Optional, List

from nisystemlink.clients import core
from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post, delete

from . import models
from uplink import Query, Field


class TestMonitorClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration]):
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()
        super().__init__(configuration, base_path="/nitestmonitor/v2/")

    @get("")
    def api_info(self) -> models.ApiInfo:
        """Get information about the available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the `ni``/nitestmonitor``` service.
        """
        ...

    @post("products")
    def create_products(
        self, products: models.CreateProductsRequest
    ) -> models.CreateProductsPartialSuccess:
        """Creates one or more products and returns errors for failed creations.

        Args:
            products: A list of products to attempt to create.

        Returns: A list of created products, products that failed to create, and errors for
            failures.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` service of provided invalid
                arguments.
        """
        ...

    @get(
        "products",
        args=[Query("continuationToken"), Query("take"), Query("returnCount")],
    )
    def get_products(
        self,
        continuation_token: Optional[str] = None,
        take: Optional[int] = None,
        return_count: Optional[bool] = None,
    ) -> models.PagedProducts:
        """Reads a list of products.

        Args:
            continuation_token: The token used to paginate results.
            take: The number of products to get in this request.
            return_count: Whether or not to return the total number of products available.

        Returns:
            A list of products.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @get("products/{id}")
    def get_product(self, id: str) -> models.Product:
        """Retrieves a single product by id.

        Args:
            id (str): Unique ID of a products.
        Returns:
            The single product matching `id`

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @post("query-products")
    def query_products(
        self, query: models.QueryProductsRequest
    ) -> models.PagedProducts:
        """Queries for products that match the filter.

        Args:
            query : The query contains a DynamicLINQ query string in addition to other details
                about how to filter and return the list of products.

        Returns:
            A paged list of products with a continuation token to get the next page.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service or provided invalid
                arguments.
        """

        ...

    @delete("products/{id}")
    def delete_product(self, id: str) -> Optional[ApiError]:
        """Deletes a single product by id.

        Args:
            id (str): Unique ID of a product.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @post("delete-products", args=[Field("ids")])
    def delete_products(
        self, ids: List[str]
    ) -> Optional[models.DeleteProductsPartialSuccess]:
        """Deletes multiple products.

        Args:
            ids (List[str]): List of unique IDs of products.

        Returns:
            A partial success if any products failed to delete, or None if all
            products were deleted successfully.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
