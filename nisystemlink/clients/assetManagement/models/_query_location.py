from enum import Enum
from typing import List, Optional
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._error import Error

class ResponseFormat(Enum):
    """Gets or sets the return type. Valid options are "JSON" and "CSV"."""

    JSON = "JSON"

    CSV = "CSV"

class Destination(Enum):
    """Gets or sets the destination of the request."""

    INLINE = "INLINE"
    """(default) Returns the list of resources as the body of the response."""

    DOWNLOAD = "DOWNLOAD"
    """Returns the list of resources as the body of the response and indicates to the client that it should be downloaded as a file."""

    FILE_SERVICE = "FILE_SERVICE"
    """Sends the list of resources to the file ingestion service and returns the ID of the file to the client in a JSON object."""

class SystemConnection(Enum):
    """System connection of the first event"""

    APPROVED = "APPROVED"

    DISCONNECTED = "DISCONNECTED"

    CONNECTED_UPDATE_PENDING = "CONNECTED_UPDATE_PENDING"

    CONNECTED  = "CONNECTED"

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
    """Gets or sets a date time value when the start event happened. This parameter has the "ISO 8601" format in order to be considered valid."""

    start_system_connection: SystemConnection
    """Gets or sets the system connection of the first event."""

    start_asset_presence: AssetPresence
    """Gets or sets the asset presence of the first event."""

    end_timestamp: Optional[str] = None
    """Gets or sets a date time value when the end event happened. This parameter has the "ISO 8601" format in order to be considered valid."""

    end_system_connection: Optional[SystemConnection] = None

    end_asset_presence: Optional[AssetPresence] = None
    """Gets or sets the asset presence of the end event."""

class QueryLocationHistoryRequest(JsonModel):
    """Model for object containing options for querying history."""

    take: Optional[int] = None

    continuation_token: Optional[str] = None
    """Gets or sets a token which allows the user to resume a query at the next item in the matching asset location history set. When querying for asset location history, a token will be returned if a query may be continued. To obtain the next page of asset location history records, pass the token to the service on a subsequent request."""

    response_format: ResponseFormat
    """Gets or sets the return type. Valid options are "JSON" and "CSV"."""

    destination: Destination
    """Gets or sets the destination of the request. "INLINE" (default) returns the list of resources as the body of the response. "DOWNLOAD" returns the list of resources as the body of the response and indicates to the client that it should be downloaded as a file. "FILE_SERVICE" sends the list of resources to the file ingestion service and returns the ID of the file to the client in a JSON object."""

    file_ingestion_workspace: Optional[str] = None
    """Gets or sets the ID of the workspace to put the file into, if the destination is "FILE_SERVICE"."""

    location_filter: Optional[str] = None
    """Gets or sets the filter criteria for location. Consists of a string of queries composed using AND/OR operators. String values and date strings need to be enclosed in double quotes. Parenthesis can be used around filters to better define the order of operations. Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'

        Operators:

            Equals operator '='. Example: 'x = y'
            Not equal operator '!='. Example: 'x != y'
            Greater than operator '>'. Example: 'x > y'
            Greater than or equal operator '>='. Example: 'x >= y'
            Less than operator '<'. Example: 'x < y'
            Less than or equal operator '<='. Example: 'x <= y'
            Logical AND operator 'and'. Example: 'x and y'
            Logical OR operator 'or'. Example: 'x or y'
            Contains operator '.Contains()', used to check whether a string contains another string. Example: 'x.Contains(y)'
            Does not contain operator '!.Contains()', used to check whether a string does not contain another string. Example: '!x.Contains(y)'
            
        Valid location properties that can be used in the filter:

            MinionId: String representing the minion id of the location of an asset.
            PhysicalLocation: String representing the physical location of the location of an asset.
            Parent: String representing the parent of the location of an asset.
            SlotNumber: Integer representing the slot number of the location of an asset."""
    
    start_time: Optional[str] = None

    end_time: Optional[str] = None

class ConnectionHistoryResponse(JsonModel):

    error: Error

    history_items: Optional[List[ConnectionHistory]] = None

    continuation_token: Optional[str] = None
    """Gets or sets a token which allows the user to resume a query at the next item in the matching asset location history set. When querying for asset location history, a token will be returned if a query may be continued. To obtain the next page of asset location history records, pass the token to the service on a subsequent request."""