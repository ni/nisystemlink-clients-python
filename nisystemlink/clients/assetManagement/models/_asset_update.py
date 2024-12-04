from typing import Dict, List, Optional
from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset import Asset, AssetBusType, AssetLocation, AssetType, ExternalCalibration, SelfCalibration, TemperatureSensor

class AssetUpdate(JsonModel):
    """Model for an object describing the properties for updating an asset.

        Unique Asset Identification is required to create an asset. If the id property is not specified, a set of properties are required to identify an asset. See AssetIdentificationModel for details. If the id is specified on the model, the following properties will be ignored: busType, modelName, modelNumber, vendorName, vendorNumber and serialNumber."""
    
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

    self_calibration: SelfCalibration

    is_n_i_asset: bool
    """Gets or sets whether this asset is an NI asset (true) or a third-party asset (false)."""

    id: Optional[str] = None
    """Gets or sets unique identifier of the asset."""

    location: AssetLocation
    """Model for information about the asset location, presence and the connection status of the system in which it resides."""

    external_calibration: ExternalCalibration

    workspace: Optional[str] = None
    """Gets or sets the ID of the workspace."""

    properties: Dict[str, str]
    """	Gets or sets key-value-pair metadata associated with an asset."""

    keywords: Optional[List[str]] = None
    """Gets or sets words or phrases associated with an asset."""

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

class UpdateAssetsRequest(JsonModel):
    """Model for request body containing an array of assets to update."""

    assets: Optional[List[AssetUpdate]] = None
    """Gets or sets multiple assets that should be updated. The maximum number of assets allowed per request is 1000."""

class UpdateAssetsPartialSuccessResponse(JsonModel):
    """Model for update Assets Partial Success Response."""

    error: Optional[ApiError] = None

    assets: Optional[List[Asset]] = None
    """Gets or sets array of updated assets."""

    failed: Optional[List[AssetUpdate]] = None
    """Gets or sets array of assets update requests that failed."""