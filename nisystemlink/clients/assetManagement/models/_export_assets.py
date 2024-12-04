from enum import Enum
from typing import Optional
from nisystemlink.clients.core._uplink._json_model import JsonModel

class ResponseFormat(Enum):
    """Gets or sets the return type. Valid option is "CSV"."""

    CSV = "CSV"

class Destination(Enum):
    """Gets or sets the destination of the request."""

    DOWNLOAD = "DOWNLOAD"
    """Returns the list of resources as the body of the response and indicates to the client that it should be downloaded as a file."""

    FILE_SERVICE = "FILE_SERVICE"
    """Sends the list of resources to the file ingestion service and returns the ID of the file to the client in a JSON object."""

class ExportAssetsRequest(JsonModel):

    filter: Optional[str] = None
    """Gets or sets the filter criteria for assets. Consists of a string of queries composed using AND/OR operators. String values and date strings need to be enclosed in double quotes. Parenthesis can be used around filters to better define the order of operations. Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'

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

        Valid asset properties that can be used in the filter:

            AssetIdentifier: String representing the unique identifier of an asset.
            SerialNumber: String representing the serial number of an asset.
            ModelName: String representing the model name of an asset.
            ModelNumber: Unsigned integer representing the model number of an asset.
            VendorName: String representing the vendor name of an asset.
            VendorNumber: Unsigned integer representing the vendor number of an asset.
            PartNumber: String representing the part number of an asset.
            AssetName: String representing the asset name.
            AssetType: String enumeration representing the asset type. Possible values are: GENERIC, DEVICE_UNDER_TEST, FIXTURE, SYSTEM.
            FirmwareVersion: String representing the firmware version of an asset.
            HardwareVersion: String representing the hardware version of an asset.
            BusType: String enumeration representing the bus type of an asset. Possible values are: BUILT_IN_SYSTEM, PCI_PXI, USB, GPIB, VXI, SERIAL, TCP_IP, CRIO, SCXI, CDAQ, SWITCH_BLOCK, SCC, FIRE_WIRE, ACCESSORY, CAN, SWITCH_BLOCK_DEVICE, SLSC.
            IsNIAsset: Boolean flag specifying whether the asset is an NI asset or a third-party asset.
            Keywords: Collection of string values representing asset metadata keywords. Example: 'Keywords=["keyword1", "keyword2"]'.
            Properties: Collection of key-value pairs, each key-value pair representing an asset metadata property. Example: 'Properties=["key1":"value1", "key2":"value2"]'.
            Location.MinionId: String representing the identifier of the minion in which the asset is located in.
            Location.SystemName: String representing the name of the system that the asset is located in.
            Location.SlotNumber: Unsigned integer representing the slot number the asset is located in.
            Location.AssetState.SystemConnection: String enumeration representing the connection state of the system the asset is currently located in. Possible values are: DISCONNECTED, CONNECTED. To maintain compatibility with previous versions of SystemLink, the values [APPROVED, UNSUPPORTED, ACTIVATED] are considered equivalent to DISCONNECTED and [CONNECTED_UPDATE_PENDING, CONNECTED_UPDATE_SUCCESSFUL, CONNECTED_UPDATE_FAILED] are equivalent to CONNECTED.
            Location.AssetState.AssetPresence: String enumeration representing the present status of an asset in a system. Possible values are: INITIALIZING, UNKNOWN, NOT_PRESENT, PRESENT.
            SupportsSelfCalibration: Boolean flag specifying whether the asset supports self-calibration.
            SelfCalibration.CalibrationDate: ISO-8601 formatted timestamp string specifying the last date the asset was self-calibrated. Example: "2018-05-20T00:00:00Z"
            SupportsExternalCalibration: Boolean flag specifying whether the asset supports external calibration.
            CalibrationStatus: String enumeration representing the calibration status of an asset. Possible values are: OK, APPROACHING_RECOMMENDED_DUE_DATE, PAST_RECOMMENDED_DUE_DATE, OUT_FOR_CALIBRATION.
            ExternalCalibration.CalibrationDate: ISO-8601 formatted timestamp string specifying the last date the asset was externally-calibrated. Example: "2018-05-20T00:00:00Z"
            ExternalCalibration.NextRecommendedDate: ISO-8601 formatted timestamp string specifying the recommended date for the next external calibration. Example: "2018-05-20T00:00:00Z". This value is overwritten by the NextCustomDueDate if it is set, otherwise it is calculated based on the RecommendedInterval.
            ExternalCalibration.RecommendedInterval: Integer representing the manufacturer-recommended calibration interval, in months.
            ExternalCalibration.Comments: String representing any external calibration comments.
            ExternalCalibration.IsLimited: Boolean flag specifying whether the last external calibration was a limited calibration.
            ExternalCalibration.Operator.DisplayName: String representing the name of the operator which performed an external calibration on a third-party asset."""
    
    response_format: ResponseFormat
    """Gets or sets the return type. Valid option is "CSV"."""

    destination: Destination
    """Gets or sets the destination of the request. "DOWNLOAD" returns the list of resources as the body of the response and indicates to the client that it should be downloaded as a file. "FILE_SERVICE" sends the list of resources to the file ingestion service and returns the ID of the file to the client in a JSON object."""

    file_ingestion_workspace: Optional[str] = None
    """Gets or sets the ID of the workspace to put the file into, if the destination is "FILE_SERVICE"."""

class ExportAssetsResponse(JsonModel):

    file_id: Optional[str] = None
    """Gets or sets file identifier in the file ingestion service."""