"""Model for asset identification."""

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._asset_types import AssetBusType


class AssetIdentification(JsonModel):
    """Model for object containing properties which identify an asset.

    An asset is uniquely identified by a combination of:

    * ``bus_type``
    * ``model_name`` or ``model_number``
    * ``vendor_name`` or ``vendor_number``
    * ``serial_number``
    """

    model_name: str | None = None
    """Model name of the asset."""

    model_number: int | None = None
    """Model number of the asset."""

    serial_number: str | None = None
    """Serial number of the asset."""

    vendor_name: str | None = None
    """Vendor name of the asset."""

    vendor_number: int | None = None
    """Vendor number of the asset."""

    bus_type: AssetBusType | None = None
    """Bus type for the asset."""
