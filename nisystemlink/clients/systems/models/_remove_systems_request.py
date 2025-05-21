from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class RemoveSystemsRequest(JsonModel):
    """Model for request to unregister systems from the server."""

    tgt: List[str]
    """Gets or sets array of strings representing the IDs of systems to remove from SystemLink."""
