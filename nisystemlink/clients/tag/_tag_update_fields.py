# -*- coding: utf-8 -*-

"""Implementation of TagUpdateFields."""

import sys

if sys.version_info < (3, 6):
    import aenum as enum  # type: ignore
else:
    import enum


class TagUpdateFields(enum.IntFlag):
    """Represents the various :class:`TagData` fields that may be included in a :class:`TagDataUpdate`.

    Fields that aren't included are left unmodified when updates are sent to the server.
    """

    KEYWORDS = 1
    """Specify that entries in the :attr:`TagData.keywords` that are missing from the
    tag's metadata on the server will be added.
    """

    PROPERTIES = 2
    """Specify that entries in the :attr:`TagData.properties` that are missing from or
    different in the tag's metadata on the server will be added or replaced.
    """

    COLLECT_AGGREGATES = 4
    """Specify that the tag's :attr:`TagData.collect_aggregates` setting will be modified on the server."""

    RETENTION = 8
    """Specify that the tag's :attr:`TagData.retention_type`,
    :attr:`TagData.retention_count`, and :attr:`TagData.retention_days` settings will be
    modified on the server.
    """

    ALL = 15
    """Specify that all fields in the :class:`TagData` should be included in the update.

    Keywords and properties that already exist on the server will not be removed, even
    if they are missing from the update.
    """
