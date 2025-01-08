from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class Package(JsonModel):
    """Model for object defining a package containing the name and version."""

    name: Optional[str] = None
    """Gets or sets name of the package."""

    version: Optional[str] = None
    """Gets or sets version of the package."""

    installRecommends: bool
    """Gets or sets a boolean variable whose value controls the installation of the recommended packages.

    This property is available starting with version 2 of the getStates and createOrUpdateStates operations.
    """
