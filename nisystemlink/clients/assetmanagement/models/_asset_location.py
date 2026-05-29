from enum import Enum

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AssetPresenceStatus(Enum):
    """Status of an asset's presence in a system."""

    INITIALIZING = "INITIALIZING"
    UNKNOWN = "UNKNOWN"
    NOT_PRESENT = "NOT_PRESENT"
    PRESENT = "PRESENT"


class SystemConnection(Enum):
    """Whether the minion is connected to the server.

    For backward compatibility, APPROVED, UNSUPPORTED, and ACTIVATED are
    treated as DISCONNECTED. CONNECTED_UPDATE_PENDING,
    CONNECTED_UPDATE_SUCCESSFUL, and CONNECTED_UPDATE_FAILED are treated
    as CONNECTED.
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
    """Asset presence and system connection information."""

    asset_presence: AssetPresenceStatus
    """Gets or sets the status of an asset's presence in a system."""

    system_connection: SystemConnection | None = None
    """Gets or sets whether the minion is connected to the server
    and has updated it with its data.
    """


class AssetPresence(JsonModel):
    """Model for the presence of an asset."""

    asset_presence: AssetPresenceStatus
    """Gets or sets the status of an asset's presence in a system."""


class _AssetLocation(JsonModel):
    """Local model for asset location and presence information."""

    minion_id: str | None = None
    """Gets or sets identifier of the minion where the asset is located."""

    physical_location: str | None = None
    """Gets or sets the physical location of the asset."""

    parent: str | None = None
    """Gets or sets the parent of the asset."""

    resource_uri: str | None = None
    """Gets or sets identifier of a resource."""

    slot_number: int | None = None
    """Gets or sets the number of the slot in which the asset is located."""


class AssetLocation(_AssetLocation):
    """Asset location and system connection information."""

    state: AssetPresenceWithSystemConnection
    """Presence of an asset and the connection of the system in which it resides."""


class AssetLocationForCreate(_AssetLocation):
    """Asset presence information used during create."""

    state: AssetPresence
    """Model for the presence of an asset."""
