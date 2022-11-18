from nisystemlink.clients.core._uplink._json_model import JsonModel


class Operation(JsonModel):
    """Represents an operation that can be performed on a data frame."""

    available: bool
    """Whether or not the operation is available to the caller (e.g. due to permissions)."""

    version: int
    """The version of the available operation."""


class OperationsV1(JsonModel):
    """The operations available in the routes provided by the v1 HTTP API."""

    create_tables: Operation
    """The ability to create new DataFrame tables."""

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
