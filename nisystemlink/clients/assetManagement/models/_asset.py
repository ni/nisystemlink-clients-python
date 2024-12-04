from enum import Enum
from typing import Dict, List, Optional
from nisystemlink.clients.core._uplink._json_model import JsonModel

class AssetBusType(Enum):
    """All supported bus types for an asset."""

    BUILT_IN_SYSTEM = "BUILT_IN_SYSTEM"

    PCI_PXI = "PCI_PXI"

    USB = "USB"

    GPIB = "GPIB"

    VXI = "VXI"

    SERIAL = "SERIAL"

    TCP_IP = "TCP_IP"

    CRIO = "CRIO"

    SCXI = "SCXI"

    CDAQ = "CDAQ"
    
    SWITCH_BLOCK = "SWITCH_BLOCK"

    SCC = "SCC"

    FIRE_WIRE = "FIRE_WIRE"

    ACCESSORY = "ACCESSORY"

    CAN = "CAN"

    SWITCH_BLOCK_DEVICE = "SWITCH_BLOCK_DEVICE"

    SLSC  = "SLSC"

class AssetType(Enum):
    """All supported asset types."""

    GENERIC =  "GENERIC"

    DEVICE_UNDER_TEST = "DEVICE_UNDER_TEST"

    FIXTURE = "FIXTURE"

    SYSTEM  = "SYSTEM"

class AssetDiscoveryType(Enum):
    """All discovery types."""

    MANUAL = "MANUAL"

    AUTOMATIC = "AUTOMATIC"

class TemperatureSensor(JsonModel):
    """Temperature sensor information."""

    name: Optional[str] = None
    """Gets or sets sensor name."""

    reading: float
    """Gets or sets sensor reading."""

class AssetPresence(Enum):
    """Status of an asset's presence in a system."""

    NOT_PRESENT = "NOT_PRESENT"

    PRESENT = "PRESENT"

    INITIALIZING = "INITIALIZING"

    UNKNOWN  = "UNKNOWN"

class SystemConnection(Enum):
    """Whether or not the minion is connected to the server and has updated the server with its data."""

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

    asset_presence: AssetPresence
    """Gets or sets the status of an asset's presence in a system."""

    system_connection: Optional[SystemConnection] = None
    """Gets or sets whether or not the minion is connected to the server and has updated the server with its data."""

class AssetLocation(JsonModel):
    """Model for information about the asset location, presence and the connection status of the system in which it resides."""

    minion_id: Optional[str] = None
    """Gets or sets identifier of the minion where the asset is located."""

    physical_location: Optional[str] = None
    """Gets or sets the physical location of the asset. An asset can be either in a system, in which case it has a MinionID, or be in a physical location."""

    parent: Optional[str] = None
    """Gets or sets the parent of the asset."""

    resource_uri: Optional[str] = None
    """Gets or sets identifier of a resource."""

    slot_number: Optional[int] = None
    """Gets or sets the number of the slot in which the asset is located."""

    state: AssetPresenceWithSystemConnection
    """Presence of an asset and the connection of the system in which it resides."""

class SelfCalibration(JsonModel):
    temperature_sensors: Optional[List[TemperatureSensor]] = None
    """Gets or sets an array of temperature sensor information. The maximum number of temperature sensors allowed per self calibration is 1000."""

    is_limited: Optional[bool] = None
    """Gets or sets whether the last self-calibration of the asset was a limited calibration."""

    date: str
    """Gets or sets ISO-8601 formatted timestamp specifying the last date the asset was self-calibrated."""

class CalibrationStatus(Enum):
    """Calibration category the asset belongs to based on the next due calibration date."""

    OK = "OK"

    APPROACHING_RECOMMENDED_DUE_DATE = "APPROACHING_RECOMMENDED_DUE_DATE"

    PAST_RECOMMENDED_DUE_DATE = "PAST_RECOMMENDED_DUE_DATE"

    OUT_FOR_CALIBRATION = "OUT_FOR_CALIBRATION"

class CalibrationEntryType(Enum):
    """Whether SystemLink automatically discovered the calibration data for an asset or if it was manually entered."""

    AUTOMATIC = "AUTOMATIC"

    MANUAL = "MANUAL"

class ExternalCalibration(JsonModel):
    temperature_sensors: Optional[List[TemperatureSensor]] = None
    """Gets or sets an array of temperature sensor information."""

    is_limited: Optional[bool] = None
    """Gets or sets whether the last external calibration of the asset was a limited calibration."""

    date: str
    """Gets or sets ISO-8601 formatted timestamp specifying the last date the asset was externally calibrated."""

    recommended_interval: int
    """Gets or sets the manufacturer's recommended calibration interval in months."""

    next_recommended_date: str
    """Gets or sets ISO-8601 formatted timestamp specifying the recommended date for the next external calibration."""

    next_custom_due_date: Optional[str] = None
    """Gets or sets ISO-8601 formatted timestamp specifying the date for the next external calibration."""

    resolved_due_date: Optional[str] = None
    """Gets ISO-8601 formatted timestamp specifying the resolved due date for external calibration. This takes into account NextCustomDueDate, Asset.CustomCalibrationInterval and NextRecommendedDate."""

    comments: Optional[str] = None
    """Gets or sets calibration comments provided by an operator."""

    entry_type: Optional[CalibrationEntryType] = None
    """Gets or sets whether SystemLink automatically discovered the calibration data for an asset or if it was manually entered."""

class Asset(JsonModel):
    """Model for an object describing an asset with all of its properties."""

    model_name: Optional[str] = None
    """Gets or sets model name of the asset."""

    model_number: int
    """Gets or sets model number of the asset."""

    serial_number: Optional[str] = None
    """Gets or sets serial number of the asset."""

    vendor_name: Optional[str] = None
    """Gets or sets vendor name of the asset."""
    
    vendor_number: int
    """Gets or sets vendor number of the asset."""

    bus_type: AssetBusType
    """Gets or sets all supported bus types for an asset."""

    name: Optional[str] = None
    """Gets or sets name of the asset."""

    asset_type: AssetType
    """Gets or sets all supported asset types."""

    discovery_type: AssetDiscoveryType
    """Gets or sets the discovery type."""

    firmware_version: Optional[str] = None
    """Gets or sets firmware version of the asset."""

    hardware_version: Optional[str] = None
    """Gets or sets hardware version of the asset."""

    visa_resource_name: Optional[str] = None
    """Gets or sets VISA resource name of the asset."""

    temperature_sensors: Optional[List[TemperatureSensor]] = None
    """Gets or sets an array of temperature sensor information."""

    supports_self_calibration: bool
    """Gets or sets whether the asset supports self-calibration."""

    supports_external_calibration: bool
    """Gets or sets whether the asset supports external calibration."""

    custom_calibration_interval: Optional[int] = None
    """Gets or sets the interval represented in months used for computing calibration due date. If not set, the recommended calibration interval from the calibration model is used."""

    self_calibration: Optional[SelfCalibration] = None

    is_n_i_asset: bool
    """Gets or sets whether this asset is an NI asset (true) or a third-party asset (false)."""

    id: Optional[str] = None
    """Gets or sets unique identifier of the asset."""

    location: AssetLocation
    """Model for information about the asset location, presence and the connection status of the system in which it resides."""

    calibration_status: Optional[CalibrationStatus] = None
    """Gets or sets the calibration category the asset belongs to based on the next due calibration date."""

    is_system_controller: bool
    """Gets or sets whether this asset represents a System Controller."""

    external_calibration: Optional[ExternalCalibration] = None

    workspace: Optional[str] = None
    """Gets or sets the ID of the workspace."""

    properties: Dict[str, str]
    """	Gets or sets key-value-pair metadata associated with an asset."""

    keywords: Optional[List[str]] = None
    """Gets or sets words or phrases associated with an asset."""

    last_updated_timestamp: str
    """Gets or sets ISO-8601 formatted timestamp specifying the last date that the asset has had a property update."""

    file_ids: Optional[List[str]] = None
    """Gets or sets all files linked to the asset."""

    supports_self_test: bool
    """Gets or sets whether the asset supports self-test."""

    supports_reset: bool
    """Gets or sets whether the asset supports reset."""

    part_number: Optional[str] = None
    """Gets or sets part number of the asset."""

    out_for_calibration: Optional[bool] = None
    """Get or set whether the asset is out for calibration."""