# -*- coding: utf-8 -*-

"""Implementation of ITimeStamper."""

import abc
import datetime


class ITimeStamper(abc.ABC):
    """Represents an object for time-stamping objects or actions such that no two
    timestamps returned by the instance are within the same microsecond.
    """

    @property
    @abc.abstractmethod
    def timestamp(self) -> datetime.datetime:  # noqa: D401
        """A unique UTC ``datetime.datetime`` that is close to the current date and time."""
        ...
