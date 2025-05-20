from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class OrderBy(Enum):
    """Field by which assets can be ordered/sorted. If OrderBy is not specified, no sorting will applied."""

    LAST_UPDATED_TIMESTAMP = "LAST_UPDATED_TIMESTAMP"


class AssetField(str, Enum):
    """Model for an object describing an asset with all of its properties."""

    MODEL_NAME = "modelName"

    MODEL_NUMBER = "modelNumber"

    SERIAL_NUMBER = "serialNumber"

    VENDOR_NAME = "vendorName"

    VENDOR_NUMBER = "vendorNumber"

    BUS_TYPE = "busType"

    NAME = "name"

    ASSET_TYPE = "assetType"

    DISCOVERY_TYPE = "discoveryType"

    FIRMWARE_VERSION = "firmwareVersion"

    HARDWARE_VERSION = "hardwareVersion"

    VISA_RESOURCE_NAME = "visaResourceName"

    TEMPERATURE_SENSORS = "temperatureSensors"

    SUPPORTS_SELF_CALIBRATION = "supportsSelfCalibration"

    SUPPORTS_EXTERNAL_CALIBRATION = "supportsExternalCalibration"

    CUSTOM_CALIBRATION_INTERVAL = "customCalibrationInterval"

    SELF_CALIBRATION = "selfCalibration"

    IS_NI_ASSET = "isNIAsset"

    ID = "id"

    LOCATION = "location"

    CALIBRATION_STATUS = "calibrationStatus"

    IS_SYSTEM_CONTROLLER = "isSystemController"

    EXTERNAL_CALIBRATION = "externalCalibration"

    WORKSPACE = "workspace"

    PROPERTIES = "properties"

    KEYWORDS = "keywords"

    LAST_UPDATE = "lastUpdatedTimestamp"

    FILES_IDS = "fileIds"

    SUPPORTS_SELF_RESET = "supportsSelfTest"

    SUPPORTS_RESET = "supportsReset"

    PART_NUMBER = "partNumber"

    OUT_FOR_CALIBRATION = "outForCalibration"


class QueryAssetsRequest(JsonModel):
    """Model for object containing filters to apply when retrieving assets."""

    ids: Optional[List[str]] = None
    """Gets or sets identifiers of the assets to be retrieved."""

    projection: List[AssetField] = []
    """
    Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """

    skip: Optional[int] = None
    """Gets or sets the number of resources to skip in the result when paging."""

    take: Optional[int] = None
    """Gets or sets how many resources to return in the result, or -1 to use a default defined by the service."""

    order_by: Optional[OrderBy] = None
    """Field by which assets can be ordered/sorted. If OrderBy is not specified, no sorting will applied."""

    descending: Optional[bool] = None
    """Whether to return the assets in the descending order. If OrderBy is not specified, this property is ignored."""

    calibratable_only: Optional[bool] = None
    """Gets or sets whether to generate a report with calibrated asset specific columns:"""

    returnCount: Optional[bool] = None
    """
    Gets or sets Whether to return the total number of assets which match the provided filter,
    disregarding the take value.
    """

    filter: Optional[str] = None
    """Gets or sets the filter criteria for assets. Consists of a string of queries composed using AND/OR operators."""


class _QueryAssetRequest(JsonModel):
    """Model for object containing filters to apply when retrieving assets."""

    ids: Optional[List[str]] = None
    """Gets or sets identifiers of the assets to be retrieved."""

    projection: Optional[str] = None
    """
    Gets or sets the projection to be used when retrieving the assets. If not specified,
    all properties will be returned.
    """

    skip: Optional[int] = None
    """Gets or sets the number of resources to skip in the result when paging."""

    take: Optional[int] = None
    """Gets or sets how many resources to return in the result, or -1 to use a default defined by the service."""

    order_by: Optional[OrderBy] = None
    """Field by which assets can be ordered/sorted. If OrderBy is not specified, no sorting will applied."""

    descending: Optional[bool] = None
    """Whether to return the assets in the descending order. If OrderBy is not specified, this property is ignored."""

    calibratable_only: Optional[bool] = None
    """Gets or sets whether to generate a report with calibrated asset specific columns:"""

    returnCount: Optional[bool] = None
    """
    Gets or sets Whether to return the total number of assets which match the provided filter,
    disregarding the take value.
    """

    filter: Optional[str] = None
    """Gets or sets the filter criteria for assets. Consists of a string of queries composed using AND/OR operators."""
