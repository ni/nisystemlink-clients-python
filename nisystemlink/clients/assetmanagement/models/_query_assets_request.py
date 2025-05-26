from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class OrderBy(Enum):
    """Field by which assets can be ordered/sorted. If OrderBy is not specified, no sorting will applied."""

    LAST_UPDATED_TIMESTAMP = "LAST_UPDATED_TIMESTAMP"


class AssetField(str, Enum):
    """Model for an object describing an asset with all of its properties."""

    MODEL_NAME = "MODEL_NAME"
    MODEL_NUMBER = "MODEL_NUMBER"
    SERIAL_NUMBER = "SERIAL_NUMBER"
    VENDOR_NAME = "VENDOR_NAME"
    VENDOR_NUMBER = "VENDOR_NUMBER"
    BUS_TYPE = "BUS_TYPE"
    NAME = "NAME"
    ASSET_TYPE = "ASSET_TYPE"
    DISCOVERY_TYPE = "DISCOVERY_TYPE"
    FIRMWARE_VERSION = "FIRMWARE_VERSION"
    HARDWARE_VERSION = "HARDWARE_VERSION"
    VISA_RESOURCE_NAME = "VISA_RESOURCE_NAME"
    TEMPERATURE_SENSORS = "TEMPERATURE_SENSORS"
    SUPPORTS_SELF_CALIBRATION = "SUPPORTS_SELF_CALIBRATION"
    SUPPORTS_EXTERNAL_CALIBRATION = "SUPPORTS_EXTERNAL_CALIBRATION"
    CUSTOM_CALIBRATION_INTERVAL = "CUSTOM_CALIBRATION_INTERVAL"
    SELF_CALIBRATION = "SELF_CALIBRATION"
    IS_NI_ASSET = "IS_NI_ASSET"
    ID = "ID"
    LOCATION = "LOCATION"
    CALIBRATION_STATUS = "CALIBRATION_STATUS"
    IS_SYSTEM_CONTROLLER = "IS_SYSTEM_CONTROLLER"
    EXTERNAL_CALIBRATION = "EXTERNAL_CALIBRATION"
    WORKSPACE = "WORKSPACE"
    PROPERTIES = "PROPERTIES"
    KEYWORDS = "KEYWORDS"
    LAST_UPDATE = "LAST_UPDATE"
    FILES_IDS = "FILES_IDS"
    SUPPORTS_SELF_RESET = "SUPPORTS_SELF_RESET"
    SUPPORTS_RESET = "SUPPORTS_RESET"
    PART_NUMBER = "PART_NUMBER"
    OUT_FOR_CALIBRATION = "OUT_FOR_CALIBRATION"


class QueryAssetsRequest(JsonModel):
    """Model for object containing filters to apply when retrieving assets."""

    projection: Optional[List[AssetField]] = None
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

    return_count: Optional[bool] = None
    """
    Gets or sets Whether to return the total number of assets which match the provided filter,
    disregarding the take value.
    """

    filter: Optional[str] = None
    """Gets or sets the filter criteria for assets. Consists of a string of queries composed using AND/OR operators."""


class _QueryAssetsRequest(JsonModel):
    """Model for object containing filters to apply when retrieving assets."""

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

    return_count: Optional[bool] = None
    """
    Gets or sets Whether to return the total number of assets which match the provided filter,
    disregarding the take value.
    """

    filter: Optional[str] = None
    """Gets or sets the filter criteria for assets. Consists of a string of queries composed using AND/OR operators."""
