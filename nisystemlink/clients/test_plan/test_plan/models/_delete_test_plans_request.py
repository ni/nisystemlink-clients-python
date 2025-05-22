from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteTestPlansRequest(JsonModel):
    """Represents a request to delete one or more test plans."""

    ids: List[str]
    """List of test plan IDS of test plans to be deleted"""
