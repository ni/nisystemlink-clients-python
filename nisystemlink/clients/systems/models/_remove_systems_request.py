from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class RemoveSystemsRequest(JsonModel):
    """Model for request to unregister systems from the server."""

    tgt: List[str]
    """Gets or sets array of strings representing the IDs of systems to remove from SystemLink."""

    force: Optional[bool] = None
    """Gets or sets a Boolean which specifies whether to remove systems from the database immediately (True)
    or wait until the unregister job returns from systems (False). If True, unregister job failures are not cached.
    """
