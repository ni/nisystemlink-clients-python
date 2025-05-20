from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._asset_calibration import (
    CalibrationStatus,
    ExternalCalibration,
    SelfCalibration,
    TemperatureSensor,
)
from ._asset_location import AssetLocation
from ._asset_types import AssetBusType, AssetDiscoveryType, AssetType


class Asset(JsonModel):
    """Model for an object describing an asset with all of its properties."""

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

    bus_type: Optional[AssetBusType] = None
    """Gets or sets all supported bus types for an asset."""

    name: Optional[str] = None
    """Gets or sets name of the asset."""

    asset_type: Optional[AssetType] = None
    """Gets or sets all supported asset types."""

    discovery_type: Optional[AssetDiscoveryType] = None
    """Gets or sets the discovery type."""

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
    """Gets or sets the interval represented in months used for computing calibration due date."""

    self_calibration: Optional[SelfCalibration] = None
    """Gets or sets the last self-calibration of the asset."""

    is_NI_asset: Optional[bool] = Field(alias="isNIAsset", default=None)
    """Gets or sets whether this asset is an NI asset (true) or a third-party asset (false)."""

    id: Optional[str] = None
    """Gets or sets unique identifier of the asset."""

    location: Optional[AssetLocation] = None
    """Model for information about the asset location, presence and the connection status of the system"""

    calibration_status: Optional[CalibrationStatus] = None
    """Gets or sets the calibration category the asset belongs to based on the next due calibration date."""

    is_system_controller: Optional[bool] = None
    """Gets or sets whether this asset represents a System Controller."""

    external_calibration: Optional[ExternalCalibration] = None
    """Gets or sets the last external calibration of the asset."""

    workspace: Optional[str] = None
    """Gets or sets the ID of the workspace."""

    properties: Optional[Dict[str, str]] = None
    """	Gets or sets key-value-pair metadata associated with an asset."""

    keywords: Optional[List[str]] = None
    """Gets or sets words or phrases associated with an asset."""

    last_updated_timestamp: Optional[datetime] = None
    """Gets or sets ISO-8601 formatted timestamp specifying the last date that the asset has had a property update."""

    file_ids: Optional[List[str]] = None
    """Gets or sets all files linked to the asset."""

    supports_self_test: Optional[bool] = None
    """Gets or sets whether the asset supports self-test."""

    supports_reset: Optional[bool] = None
    """Gets or sets whether the asset supports reset."""

    part_number: Optional[str] = None
    """Gets or sets part number of the asset."""

    out_for_calibration: Optional[bool] = None
    """Get or set whether the asset is out for calibration."""
