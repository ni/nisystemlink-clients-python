from typing import Dict, List, Optional
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._error import Error
from ._asset import Asset, AssetBusType, AssetDiscoveryType, AssetLocation, AssetType, ExternalCalibration, SelfCalibration, TemperatureSensor

class AssetCreate(JsonModel):
    """Model for an object describing the properties for creating an asset. Unique Asset Identification is required to create an asset. See AssetIdentificationModel for details."""

    model_name: Optional[str] = None
    """Gets or sets model name of the asset."""

    model_number: Optional[int] = None
    """Gets or sets model number of the asset."""

    serial_number: Optional[str] = None
    """Gets or sets serial number of the asset."""

    vendor_name: Optional[str] = None
    """Gets or sets vendor name of the asset."""
    
    vendor_number: Optional[int] = None
    """Gets or sets vendor number of the asset."""

    bus_type: AssetBusType
    """Gets or sets all supported bus types for an asset."""

    name: Optional[str] = None
    """Gets or sets name of the asset."""

    asset_type: AssetType
    """Gets or sets all supported asset types."""

    firmware_version: Optional[str] = None
    """Gets or sets firmware version of the asset."""

    hardware_version: Optional[str] = None
    """Gets or sets hardware version of the asset."""

    visa_resource_name: Optional[str] = None
    """Gets or sets VISA resource name of the asset."""

    temperature_sensors: Optional[List[TemperatureSensor]] = None
    """Gets or sets an array of temperature sensor information."""

    supports_self_calibration: Optional[bool] = None
    """Gets or sets whether the asset supports self-calibration."""

    supports_external_calibration: Optional[bool] = None
    """Gets or sets whether the asset supports external calibration."""

    custom_calibration_interval: Optional[int] = None
    """Gets or sets the interval represented in months used for computing calibration due date. If not set, the recommended calibration interval from the calibration model is used."""

    self_calibration: SelfCalibration

    is_ni_asset: Optional[bool] = None
    """Gets or sets whether this asset is an NI asset (true) or a third-party asset (false)."""

    workspace: Optional[str] = None
    """Gets or sets the ID of the workspace."""

    location: AssetLocation
    """Model for information about the asset location, presence and the connection status of the system in which it resides."""

    external_calibration: ExternalCalibration

    properties: Optional[Dict[str, str]] = None
    """	Gets or sets key-value-pair metadata associated with an asset."""

    keywords: Optional[List[str]] = None
    """Gets or sets words or phrases associated with an asset."""

    discovery_type: AssetDiscoveryType
    """Gets or sets the discovery type."""

    file_ids: Optional[List[str]] = None
    """Gets or sets all files linked to the asset."""

    supports_self_test: Optional[bool] = None
    """Gets or sets whether the asset supports self-test."""

    supports_reset: Optional[bool] = None
    """Gets or sets whether the asset supports reset."""

    part_number: Optional[str] = None
    """Gets or sets part number of the asset."""

class CreateAssetsRequest(JsonModel):
    """Model for request body containing an array of assets that should be created."""

    assets: Optional[List[AssetCreate]] = None
    """Gets or sets multiple assets that should be created. The maximum number of assets allowed per request is 1000."""

class AssetsCreatePartialSuccessResponse(JsonModel):
    """Model for create Assets Partial Success Response."""

    error: Optional[Error] = None

    assets: Optional[List[Asset]] = None
    """Gets or sets array of created assets."""

    failed: Optional[List[AssetCreate]] = None
    """Gets or sets array of assets create requests that failed."""