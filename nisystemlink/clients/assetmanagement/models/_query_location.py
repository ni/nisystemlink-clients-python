from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class ResponseFormat(Enum):
    """Gets or sets the return type. Valid options are "JSON" and "CSV"."""

    JSON = "JSON"

    CSV = "CSV"


class Destination(Enum):
    """Gets or sets the destination of the request."""

    INLINE = "INLINE"
    """(default) Returns the list of resources as the body of the response."""

    DOWNLOAD = "DOWNLOAD"
    """Returns the list of resources as the body of the response and it should be downloaded as a file."""

    FILE_SERVICE = "FILE_SERVICE"
    """Sends the list of resources to the file ingestion service and returns the ID of the file in a JSON object."""


class SystemConnection(Enum):
    """System connection of the first event"""

    APPROVED = "APPROVED"

    DISCONNECTED = "DISCONNECTED"

    CONNECTED_UPDATE_PENDING = "CONNECTED_UPDATE_PENDING"

    CONNECTED = "CONNECTED"

    CONNECTED_UPDATE_FAILED = "CONNECTED_UPDATE_FAILED"

    UNSUPPORTED = "UNSUPPORTED"

    ACTIVATED = "ACTIVATED"

    CONNECTED_UPDATE_SUCCESSFUL = "CONNECTED_UPDATE_SUCCESSFUL"


class AssetPresence(Enum):
    """asset presence of the first event."""

    NOT_PRESENT = "NOT_PRESENT"

    PRESENT = "PRESENT"

    INITIALIZING = "INITIALIZING"

    UNKNOWN = "UNKNOWN"


class ConnectionHistory(JsonModel):

    id: Optional[str] = None
    """Gets or sets unique identifier of the connection history entry."""

    minion_id: Optional[str] = None
    """Gets or sets identifier of the minion where the asset is located."""

    physical_location: Optional[str] = None
    """Gets or sets identifier of the physical location where the asset is located."""

    parent: Optional[str] = None
    """Gets or sets the parent of the asset."""

    resource_uri: Optional[str] = None
    """Gets or sets identifier of a resource."""

    slot_number: int
    """Gets or sets the number of the slot in which the asset is located."""

    start_timestamp: str
    """Gets or sets a date time value when the start event happened."""

    start_system_connection: SystemConnection
    """Gets or sets the system connection of the first event."""

    start_asset_presence: AssetPresence
    """Gets or sets the asset presence of the first event."""

    end_timestamp: Optional[str] = None
    """Gets or sets a date time value when the end event happened."""

    end_system_connection: Optional[SystemConnection] = None

    end_asset_presence: Optional[AssetPresence] = None
    """Gets or sets the asset presence of the end event."""


class QueryLocationHistoryRequest(JsonModel):
    """Model for object containing options for querying history."""

    take: Optional[int] = None

    continuation_token: Optional[str] = None
    """Gets or sets a token which allows user to resume query at next item in the matching asset location history."""

    response_format: ResponseFormat
    """Gets or sets the return type. Valid options are "JSON" and "CSV"."""

    destination: Destination
    """Gets or sets the destination of the request."""

    file_ingestion_workspace: Optional[str] = None
    """Gets or sets the ID of the workspace to put the file into, if the destination is "FILE_SERVICE"."""

    location_filter: Optional[str] = None
    """Gets or sets the filter criteria for location."""

    start_time: Optional[str] = None

    end_time: Optional[str] = None


class ConnectionHistoryResponse(JsonModel):

    error: Optional[ApiError] = None

    history_items: Optional[List[ConnectionHistory]] = None

    continuation_token: Optional[str] = None
    """Gets or sets a token which allows user to resume query at next item in the matching asset location history."""
