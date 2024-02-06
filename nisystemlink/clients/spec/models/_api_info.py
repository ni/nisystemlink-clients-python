from __future__ import annotations


from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Extra


class V1Operations(JsonModel):
    """The operations available in the routes provided by the v1 HTTP API."""

    create_specifications: Operation
    query_specifications: Operation
    update_specifications: Operation
    delete_specifications: Operation


class Operation(JsonModel):
    class Config:
        extra = Extra.forbid

    available: bool
    """ Whether the operation is available to the caller """
    version: int
    """ Version of the available operation. """


V1Operations.update_forward_refs()
