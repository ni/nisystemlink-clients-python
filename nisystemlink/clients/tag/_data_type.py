# -*- coding: utf-8 -*-

"""Implementation of DataType."""

import enum


class DataType(enum.Enum):
    """Represents the different data types for a SystemLink tag."""

    UNKNOWN = 0
    """An unknown or invalid data type.

    Not a valid input to API calls, but used to represent tags whose data type isn't
    recognized.
    """

    DOUBLE = 1
    """A 64-bit floating-point tag following the IEEE standard.

    Double tags support collecting aggregate values for the min, max, mean, and count.
    """

    INT32 = 2
    """A 32-bit signed integer tag.

    Int32 tags support collecting aggregate values for the min, max, mean, and count.
    The mean is represented as a double.
    """

    STRING = 3
    """A string tag for arbitrary values.

    String tags support collecting aggregate values for the count.
    """

    BOOLEAN = 4
    """A boolean tag.

    Bool tags support collecting aggregate values for the count.
    """

    UINT64 = 5
    """A 64-bit unsigned integer tag.

    UInt64 tags support collecting aggregate values for the min, max, mean, and count.
    The mean is represented as a double value and will truncate large values.
    """

    DATE_TIME = 6
    """A date and time tag that stores values in UTC ISO 8601 format.

    DateTime tags support collecting aggregate values for the count.
    """

    @property
    def api_name(self) -> str:
        """Web API name of the enum value."""
        return _API_NAME[self]

    @classmethod
    def from_api_name(cls, name: str) -> "DataType":
        return cls(_FROM_API_NAME.get(name, cls.UNKNOWN))


_API_NAME = {
    DataType.UNKNOWN: "UNKNOWN",
    DataType.DOUBLE: "DOUBLE",
    DataType.INT32: "INT",
    DataType.STRING: "STRING",
    DataType.BOOLEAN: "BOOLEAN",
    DataType.UINT64: "U_INT64",
    DataType.DATE_TIME: "DATE_TIME",
}

_FROM_API_NAME = {
    "DOUBLE": DataType.DOUBLE,
    "INT": DataType.INT32,
    "STRING": DataType.STRING,
    "BOOLEAN": DataType.BOOLEAN,
    "U_INT64": DataType.UINT64,
    "DATE_TIME": DataType.DATE_TIME,
}
