from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class CreateVirtualSystemResponse(JsonModel):
    """Model for create virtual system response containing the minion ID of the system which is created."""

    minionId: Optional[str] = None
    """The minion ID of the created virtual system."""
