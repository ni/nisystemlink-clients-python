from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AcknowledgeByInstanceIdRequest(JsonModel):
    """Contains information about the alarms to acknowledge."""

    instance_ids: List[str]
    """The instanceIds of the alarms which should be acknowledged."""

    force_clear: Optional[bool] = False
    """Whether or not the affected alarms should have their clear field set to true."""
