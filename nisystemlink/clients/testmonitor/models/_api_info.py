from nisystemlink.clients.core._api_info import Operation
from nisystemlink.clients.core._uplink._json_model import JsonModel


class V2Operations(JsonModel):
    """The operations available in the routes provided by the v2 HTTP API."""

    get_results: Operation
    get_results_property_keys: Operation
    query_results: Operation
    create_results: Operation
    update_results: Operation
    delete_result: Operation
    delete_many_results: Operation
    get_steps: Operation
    query_steps: Operation
    create_steps: Operation
    update_steps: Operation
    delete_step: Operation
    delete_many_steps: Operation
    get_products: Operation
    query_products: Operation
    create_products: Operation
    update_products: Operation
    delete_products: Operation
    delete_many_products: Operation
    query_paths: Operation
