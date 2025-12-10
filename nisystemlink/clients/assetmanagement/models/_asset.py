from datetime import datetime
from typing import Dict, List

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

    model_name: str | None = None
    """Gets or sets model name of the asset."""

    model_number: int | None = None
    """Gets or sets model number of the asset."""

    serial_number: str | None = None
    """Gets or sets serial number of the asset."""

    vendor_name: str | None = None
    """Gets or sets vendor name of the asset."""

    vendor_number: int | None = None
    """Gets or sets vendor number of the asset."""

    bus_type: AssetBusType | None = None
    """Gets or sets all supported bus types for an asset."""

    name: str | None = None
    """Gets or sets name of the asset."""

    asset_type: AssetType | None = None
    """Gets or sets all supported asset types."""

    discovery_type: AssetDiscoveryType | None = None
    """Gets or sets the discovery type."""

    firmware_version: str | None = None
    """Gets or sets firmware version of the asset."""

    hardware_version: str | None = None
    """Gets or sets hardware version of the asset."""

    visa_resource_name: str | None = None
    """Gets or sets VISA resource name of the asset."""

    temperature_sensors: List[TemperatureSensor] | None = None
    """Gets or sets an array of temperature sensor information."""

    supports_self_calibration: bool | None = None
    """Gets or sets whether the asset supports self-calibration."""

    supports_external_calibration: bool | None = None
    """Gets or sets whether the asset supports external calibration."""

    custom_calibration_interval: int | None = None
    """Gets or sets the interval represented in months used for computing calibration due date."""

    self_calibration: SelfCalibration | None = None
    """Gets or sets the last self-calibration of the asset."""

    is_NI_asset: bool | None = Field(alias="isNIAsset", default=None)
    """Gets or sets whether this asset is an NI asset (true) or a third-party asset (false)."""

    id: str | None = None
    """Gets or sets unique identifier of the asset."""

    location: AssetLocation | None = None
    """Model for information about the asset location, presence and the connection status of the system"""

    calibration_status: CalibrationStatus | None = None
    """Gets or sets the calibration category the asset belongs to based on the next due calibration date."""

    is_system_controller: bool | None = None
    """Gets or sets whether this asset represents a System Controller."""

    external_calibration: ExternalCalibration | None = None
    """Gets or sets the last external calibration of the asset."""

    workspace: str | None = None
    """Gets or sets the ID of the workspace."""

    properties: Dict[str, str] | None = None
    """	Gets or sets key-value-pair metadata associated with an asset."""

    keywords: List[str] | None = None
    """Gets or sets words or phrases associated with an asset."""

    last_updated_timestamp: datetime | None = None
    """Gets or sets ISO-8601 formatted timestamp specifying the last date that the asset has had a property update."""

    file_ids: List[str] | None = None
    """Gets or sets all files linked to the asset."""

    supports_self_test: bool | None = None
    """Gets or sets whether the asset supports self-test."""

    supports_reset: bool | None = None
    """Gets or sets whether the asset supports reset."""

    part_number: str | None = None
    """Gets or sets part number of the asset."""

    out_for_calibration: bool | None = None
    """Get or set whether the asset is out for calibration."""
