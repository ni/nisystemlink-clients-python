from enum import Enum


class DataType(str, Enum):
    """Represents the different data types for a table column."""

    Bool = "BOOL"
    """32-bit IEEE 754 floating-point number."""

    Float32 = "FLOAT32"
    """32-bit IEEE 754 floating-point number."""

    Float64 = "FLOAT64"
    """64-bit IEEE 754 floating-point number."""

    Int32 = "INT32"
    """32-bit signed integers."""

    Int64 = "INT64"
    """64-bit signed integers."""

    String = "STRING"
    """Arbitrary string data."""

    Timestamp = "TIMESTAMP"
    """Date and time represented in UTC with millisecond precision."""
