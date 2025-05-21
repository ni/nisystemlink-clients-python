from enum import auto, Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class OrderBy(Enum):
    """Field by which assets can be ordered/sorted. If OrderBy is not specified, no sorting will applied."""

    LAST_UPDATED_TIMESTAMP = "LAST_UPDATED_TIMESTAMP"


class AssetField(str, Enum):
    """Model for an object describing an asset with all of its properties."""

    MODEL_NAME = auto()

    MODEL_NUMBER = auto()

    SERIAL_NUMBER = auto()

    VENDOR_NAME = auto()

    VENDOR_NUMBER = auto()

    BUS_TYPE = auto()

    NAME = auto()

    ASSET_TYPE = auto()

    DISCOVERY_TYPE = auto()

    FIRMWARE_VERSION = auto()

    HARDWARE_VERSION = auto()

    VISA_RESOURCE_NAME = auto()

    TEMPERATURE_SENSORS = auto()

    SUPPORTS_SELF_CALIBRATION = auto()

    SUPPORTS_EXTERNAL_CALIBRATION = auto()

    CUSTOM_CALIBRATION_INTERVAL = auto()

    SELF_CALIBRATION = auto()

    IS_NI_ASSET = auto()

    ID = auto()

    LOCATION = auto()

    CALIBRATION_STATUS = auto()

    IS_SYSTEM_CONTROLLER = auto()

    EXTERNAL_CALIBRATION = auto()

    WORKSPACE = auto()

    PROPERTIES = auto()

    KEYWORDS = auto()

    LAST_UPDATE = auto()

    FILES_IDS = auto()

    SUPPORTS_SELF_RESET = auto()

    SUPPORTS_RESET = auto()

    PART_NUMBER = auto()

    OUT_FOR_CALIBRATION = auto()


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


class _QueryAssetRequest(JsonModel):
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
