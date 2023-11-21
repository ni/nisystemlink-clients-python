from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteMutipleRequest(JsonModel):
    """The description of files to delete."""

    ids: List[str]
    """The list of file IDs to delete."""
