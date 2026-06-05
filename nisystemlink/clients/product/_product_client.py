"""Implementation of Product Client"""

from typing import List

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from uplink import Field, Query, retry, returns

from . import models
from ..core.helpers._partial_success import unwrap_single_item_partial_success


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class ProductClient(BaseClient):
    def __init__(self, configuration: core.HttpConfiguration | None = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Product Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()
        super().__init__(configuration, base_path="/nitestmonitor/v2/")

    @post("products", args=[Field("products")])
    def create_products(
        self, products: List[models.CreateProductRequest]
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

    def create_product(self, product: models.CreateProductRequest) -> models.Product:
        """Creates a single product.

        Args:
            product: The product to create.

        Returns:
            The created product.

        Raises:
            ApiException: if the product could not be created or the service returns an
                unexpected partial-success payload.
        """
        response = self.create_products([product])

        return unwrap_single_item_partial_success(
            response=response,
            items=response.products,
            failed=response.failed,
            error=response.error,
            failure_message="Failed to create product.",
            empty_message="Server returned no created products.",
        )

    @get(
        "products",
        args=[Query("continuationToken"), Query("take"), Query("returnCount")],
    )
    def get_products_paged(
        self,
        continuation_token: str | None = None,
        take: int | None = None,
        return_count: bool | None = None,
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
    def query_products_paged(
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

    @returns.json  # type: ignore
    @post("query-product-values")
    def query_product_values(
        self, query: models.QueryProductValuesRequest
    ) -> List[str]:
        """Queries for products that match the query and returns a list of the requested field.

        Args:
            query : The query for the fields you want.

        Returns:
            A list of the values of the field you requested.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service or provided
            invalid arguments.
        """
        ...

    @post("update-products", args=[Field("products"), Field("replace")])
    def update_products(
        self, products: List[models.UpdateProductRequest], replace: bool = False
    ) -> models.CreateProductsPartialSuccess:
        """Updates a list of products with optional field replacement.

        Args:
            `products`: A list of products to update. Products are matched for update by id.
            `replace`: Replace the existing fields instead of merging them. Defaults to `False`.
                If this is `True`, then `keywords` and `properties` for the product will be
                    replaced by what is in the `products` provided in this request.
                If this is `False`, then the `keywords` and `properties` in this request will
                    merge with what is already present in the server resource.

        Returns: A list of updates products, products that failed to update, and errors for
            failures.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    def update_product(
        self, product: models.UpdateProductRequest, replace: bool = False
    ) -> models.Product:
        """Updates a single product.

        Args:
            product: The product to update.
            replace: Replace the existing fields instead of merging them.

        Returns:
            The updated product.

        Raises:
            ApiException: if the product could not be updated or the service returns an
                unexpected partial-success payload.
        """
        response = self.update_products([product], replace=replace)

        return unwrap_single_item_partial_success(
            response=response,
            items=response.products,
            failed=response.failed,
            error=response.error,
            failure_message="Failed to update product.",
            empty_message="Server returned no updated products.",
        )

    @delete("products/{id}")
    def delete_product(self, id: str) -> None:
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
    ) -> models.DeleteProductsPartialSuccess | None:
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
        ...
