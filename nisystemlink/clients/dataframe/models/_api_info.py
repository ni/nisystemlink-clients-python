from nisystemlink.clients.core._api_info import Operation
from nisystemlink.clients.core._uplink._json_model import JsonModel


class OperationsV1(JsonModel):
    """The operations available in the routes provided by the v1 HTTP API."""

    create_tables: Operation
    """The ability to create new data tables."""

    delete_tables: Operation
    """The ability to delete tables and all of their data."""

    modify_metadata: Operation
    """The ability to modify metadata for tables."""

    list_tables: Operation
    """The ability to locate and read metadata for tables."""

    read_data: Operation
    """The ability to query and read data from tables."""

    write_data: Operation
    """The ability to append rows of data to tables."""


class ApiInfo(JsonModel):
    """Information about the available API operations."""

    operations: OperationsV1
