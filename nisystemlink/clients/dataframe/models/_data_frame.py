from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class DataFrame(JsonModel):
    """Data read from or to be written to a table.

    Values may be ``None`` (if the column is of type ``NULLABLE``) or encoded as
    a string in a format according to each column's datatype:

    * BOOL: One of ``"true"`` or ``"false"``, case-insensitive.
    * INT32: Any integer number in the range [-2147483648, 2147483647],
      surrounded by quotes.
    * INT64: Any integer number in the range [-9223372036854775808,
      9223372036854775807], surrounded by quotes.
    * FLOAT32: A decimal number using a period for the decimal point, optionally
      in scientific notation, in the range [-3.40282347E+38, 3.40282347E+38],
      surrounded by quotes. Not all values within the range can be represented
      with 32 bits. To preserve the exact binary encoding of the value when
      converting to a string, clients should serialize 9 digits after the
      decimal. Instead of a number, the value may be ``"NaN"`` (not a number),
      ``"Infinity"`` (positive infinity), or ``"-Infinity"`` (negative
      infinity), case-sensitive.
    * FLOAT64: A decimal number using a period for the decimal point, optionally
      in scientific notation, in the range [-1.7976931348623157E+308,
      1.7976931348623157E+308], surrounded by quotes. Not all values within the
      range can be represented with 64 bits. To preserve the exact binary
      encoding of the value when converting to a string, clients should
      serialize 17 digits after the decimal. Instead of a number, the value may
      be ``"NaN"`` (not a number), ``"Infinity"`` (positive infinity), or
      ``"-Infinity"`` (negative infinity), case-sensitive.
    * STRING: Any quoted string.
    * TIMESTAMP: A date and time with millisecond precision in ISO-8601 format
      and time zone. For example: ``"2022-08-19T16:17:30.123Z"``. If a time zone
      is not provided, UTC is assumed. If a time zone other than UTC is
      provided, the value will be converted to UTC. If more than three digits of
      fractional seconds are provided, the time will be truncated to three
      digits (i.e. milliseconds).

    The format is the same as a serialized Pandas DataFrame with orient="split"
    and index=False. See
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html.

    When providing a DataFrame for appending rows, any of the table's columns
    not specified will receive a value of ``None``. If any such columns aren't
    nullable, an error will be returned. If the entire columns property is left
    out, each row is assumed to contain all columns in the order specified when
    the table was created.
    """

    columns: Optional[List[str]] = None
    """The names and order of the columns included in the data frame."""

    data: List[List[Optional[str]]]
    """The data for each row with the order specified in the columns property.
    Must contain a value for each column in the columns property."""
