from nisystemlink.clients.core._uplink._json_model import JsonModel


class Operation(JsonModel):
    """Represents an operation that can be performed on a data frame."""

    available: bool
    version: int


class OperationsV1(JsonModel):
    """The operations available in the routes provided by the v1 HTTP API."""

    create_tables: Operation
    delete_tables: Operation
    modify_metadata: Operation
    list_tables: Operation
    read_data: Operation
    write_data: Operation


class ApiInfo(JsonModel):
    """Information about the available API operations."""

    operations: OperationsV1
