from enum import Enum


class Architecture(Enum):
    """Supported architecture by a state"""

    ARM = "ARM"

    X64 = "X64"

    X86 = "X86"

    ANY = "ANY"
