from nisystemlink.clients.core._uplink._json_model import JsonModel


class Operation(JsonModel):
    """Represents an operation that can be performed on a specification."""

    available: bool
    """ Whether the operation is available to the caller """

    version: int
    """ Version of the available operation. """


class V1Operations(JsonModel):
    """The operations available in the routes provided by the v1 HTTP API."""

    create_specifications: Operation
    """The ability to create new specifications."""

    query_specifications: Operation
    """The ability to query specifications."""

    update_specifications: Operation
    """The ability to update specifications."""

    delete_specifications: Operation
    """The ability to delete specifications."""
