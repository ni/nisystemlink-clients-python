from nisystemlink.clients.core._uplink._json_model import JsonModel


class Operation(JsonModel):
    """Represents an operation that can be performed on a data frame."""

    available: bool
    """Whether or not the operation is available to the caller (e.g. due to permissions)."""

    version: int
    """The version of the available operation."""
