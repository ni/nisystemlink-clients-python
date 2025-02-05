from enum import Enum


class Distribution(Enum):
    """Supported distribution by a state"""

    NI_LINUXRT = "NI_LINUXRT"

    NI_LINUXRT_NXG = "NI_LINUXRT_NXG"

    WINDOWS = "WINDOWS"

    ANY = "ANY"
