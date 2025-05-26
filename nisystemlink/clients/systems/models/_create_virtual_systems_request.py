from nisystemlink.clients.core._uplink._json_model import JsonModel


class CreateVirtualSystemRequest(JsonModel):
    """Model for create virtual system response containing the minion ID of the system which is created."""

    alias: str
    """Alias of the virtual system."""

    workspace: str
    """Workspace to create the virtual system in."""
