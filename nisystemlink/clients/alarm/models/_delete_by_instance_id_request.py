from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteByInstanceIdRequest(JsonModel):
    """Contains information about the alarms to delete."""

    instance_ids: List[str]
    """The instanceIds of the alarms which should be deleted."""
