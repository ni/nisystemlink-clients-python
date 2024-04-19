from nisystemlink.clients.core._api_info import Operation
from nisystemlink.clients.core._uplink._json_model import JsonModel


class V2Operations(JsonModel):
    """The operations available in the routes provided by the v2 HTTP API."""

    get_products: Operation
    """The ability to get a list of products."""

    query_products: Operation
    """The ability to query products based on their properties."""

    create_products: Operation
    """The ability to create one or more products."""

    update_products: Operation
    """The ability to update the properties of one or more products."""

    delete_products: Operation
    """The ability to delete a single products."""

    delete_many_products: Operation
    """The ability to delete a list of products."""

    get_results: Operation
    """The ability to get a list of results."""

    get_results_property_keys: Operation
    """The ability to get custom property keys."""

    query_results: Operation
    """"The ability to to query results based on their properties."""

    create_results: Operation
    """The ability to create results."""

    update_results: Operation
    """The ability to update results."""

    delete_result: Operation
    """The ability to delete a single results."""

    delete_many_results: Operation
    """The ability to delete multiple results."""

    get_steps: Operation
    """The ability to get a list of steps."""

    query_steps: Operation
    """The ability to query steps based on their properties."""

    create_steps: Operation
    """The ability to create steps."""

    update_steps: Operation
    """The ability to update steps."""

    delete_step: Operation
    """The ability to delete a single step."""

    delete_many_steps: Operation
    """The ability to delete multiple steps."""

    query_paths: Operation
    """The ability to query step paths."""


class ApiInfo(JsonModel):
    """Information about the available API operations."""

    operations: V2Operations
