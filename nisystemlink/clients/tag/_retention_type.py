# -*- coding: utf-8 -*-

"""Implementation of RetentionType."""

import enum


class RetentionType(enum.Enum):
    """Represents the different ways for the SystemLink tag historian to retain the history of tag values."""

    INVALID = 0
    """An unknown or invalid tag retention type.

    Not a valid input to API calls, but used to represent tags whose retention type
    isn't recognized.
    """

    NONE = 1
    """No history for the tag's value is retained."""

    DURATION = 2
    """Historical values for the tag are retained for a set number of days."""

    COUNT = 3
    """A set number of historical values for the tag are retained."""

    PERMANENT = 4
    """All of the tag's values are retained until the tag is deleted."""
