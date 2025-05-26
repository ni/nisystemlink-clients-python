from enum import Enum
from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AssetPresenceStatus(Enum):
    """Status of an asset's presence in a system."""

    INITIALIZING = "INITIALIZING"
    UNKNOWN = "UNKNOWN"
    NOT_PRESENT = "NOT_PRESENT"
    PRESENT = "PRESENT"


class SystemConnection(Enum):
    """Whether or not the minion is connected to the server and has updated the server with its data.
    To maintain compatibility with previous versions of SystemLink, the values
    [APPROVED, UNSUPPORTED, ACTIVATED] are considered equivalent to DISCONNECTED and
    [CONNECTED_UPDATE_PENDING, CONNECTED_UPDATE_SUCCESSFUL, CONNECTED_UPDATE_FAILED] are equivalent to CONNECTED.
    """

    APPROVED = "APPROVED"
    DISCONNECTED = "DISCONNECTED"
    CONNECTED_UPDATE_PENDING = "CONNECTED_UPDATE_PENDING"
    CONNECTED = "CONNECTED"
    CONNECTED_UPDATE_FAILED = "CONNECTED_UPDATE_FAILED"
    UNSUPPORTED = "UNSUPPORTED"
    ACTIVATED = "ACTIVATED"
    CONNECTED_UPDATE_SUCCESSFUL = "CONNECTED_UPDATE_SUCCESSFUL"


class AssetPresenceWithSystemConnection(JsonModel):
    """Model for the presence of an asset and the connection of the system in which it resides."""

    asset_presence: AssetPresenceStatus
    """Gets or sets the status of an asset's presence in a system."""

    system_connection: Optional[SystemConnection] = None
    """Gets or sets whether or not the minion is connected to the server and has updated the server with its data."""


class AssetPresence(JsonModel):
    """Model for the presence of an asset."""

    asset_presence: AssetPresenceStatus
    """Gets or sets the status of an asset's presence in a system."""


class _AssetLocation(JsonModel):
    """local model for information about the asset location, presence and the connection status of the system."""

    minion_id: Optional[str] = None
    """Gets or sets identifier of the minion where the asset is located."""

    physical_location: Optional[str] = None
    """Gets or sets the physical location of the asset."""

    parent: Optional[str] = None
    """Gets or sets the parent of the asset."""

    resource_uri: Optional[str] = None
    """Gets or sets identifier of a resource."""

    slot_number: Optional[int] = None
    """Gets or sets the number of the slot in which the asset is located."""


class AssetLocation(_AssetLocation):
    """Model for information about the asset location, presence and the connection status of the system."""

    state: AssetPresenceWithSystemConnection
    """Presence of an asset and the connection of the system in which it resides."""


class AssetLocationForCreate(_AssetLocation):
    """Model for information about the asset presence status of the system, used while create"""

    state: AssetPresence
    """Model for the presence of an asset."""
