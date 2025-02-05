from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class SystemImage(JsonModel):
    """Model for object defining a system image containing the name and version."""

    name: Optional[str] = None
    """Gets or sets name of the system image."""

    version: Optional[str] = None
    """Gets or sets version of the system image."""
