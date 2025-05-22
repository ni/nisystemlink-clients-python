from enum import Enum


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
    SLSC = "SLSC"


class AssetType(Enum):
    """All supported asset types."""

    GENERIC = "GENERIC"
    DEVICE_UNDER_TEST = "DEVICE_UNDER_TEST"
    FIXTURE = "FIXTURE"
    SYSTEM = "SYSTEM"


class AssetDiscoveryType(Enum):
    """All discovery types."""

    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"
