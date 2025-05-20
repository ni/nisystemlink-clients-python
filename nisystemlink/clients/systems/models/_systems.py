from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class System(JsonModel):
    """Represents the systems model."""

    id: Optional[str] = None
    """Represents id of systems."""

    alias: Optional[str] = None
    """Represents alias of the system."""

    workspace: Optional[str] = None
    """Represents the workspace associated to the system."""
