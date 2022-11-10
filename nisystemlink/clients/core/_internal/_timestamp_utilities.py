# -*- coding: utf-8 -*-

"""Implementation of TimestampUtilities."""

import datetime

from typing_extensions import final


@final
class TimestampUtilities:
    """Provides utilities for reading and writing timestamps as strings.

    Clients do not typically need to call methods on this class.
    """

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'TimestampUtilities' is not an acceptable base type")

    def __init__(self) -> None:
        raise TypeError("Can't instantiate static class 'TimestampUtilities'")

    @classmethod
    def datetime_to_str(cls, value: datetime.datetime) -> str:
        """Convert the given ``datetime.datetime`` into a string timestamp in the standard format used in SystemLink.

        Args:
            value: The date and time to convert.

        Returns:
            The string representation of the timestamp.
        """
        return datetime.datetime.utcfromtimestamp(value.timestamp()).isoformat() + "Z"

    @classmethod
    def str_to_datetime(cls, timestamp: str) -> datetime.datetime:
        """Attempt to parse a SystemLink-formatted timestamp string into a ``datetime.datetime``.

        Args:
            timestamp: The timestamp to parse, in the standard format used in
                SystemLink.

        Returns:
            The parsed datetime.

        Raises:
            ValueError: if the timestamp format is not as expected
        """
        # Python's supported ISO format requires exactly 6 digits after the
        # decimal, and doesn't support "Z" as the timezone
        # Valid format is: YYYY-MM-DDThh:mm:ss.ssssss+NN:NN
        if not timestamp.endswith("Z"):
            raise ValueError(
                "Given timestamp doesn't end with 'Z': '{}'".format(timestamp)
            )
        timestamp = timestamp[:-1].ljust(26, "0")[:26] + "+0000"
        # Note to users: this will be in UTC time; to get a local datetime, you
        # can use value.astimezone()
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
