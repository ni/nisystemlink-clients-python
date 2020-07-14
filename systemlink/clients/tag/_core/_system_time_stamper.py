# -*- coding: utf-8 -*-

"""Implementation of SystemTimeStamper."""

import datetime
import threading

from systemlink.clients.tag._core._itime_stamper import ITimeStamper
from typing_extensions import final


@final
class SystemTimeStamper(ITimeStamper):
    """A :class:`ITimeStamper` that uses the system clock."""

    _increment = datetime.timedelta(microseconds=1)

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'SystemTimeStamper' is not an acceptable base type")

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._last = datetime.datetime.now(datetime.timezone.utc)

    @property
    def timestamp(self) -> datetime.datetime:  # noqa: D401
        """A unique UTC ``datetime.datetime`` that is close to the current date and time."""
        timestamp = datetime.datetime.now(datetime.timezone.utc)

        with self._lock:
            if timestamp > self._last:
                self._last = timestamp
            else:
                self._last += self._increment
            return self._last
