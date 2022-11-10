# -*- coding: utf-8 -*-

"""Implementation of TagDataUpdate."""

from typing import Any, Dict, Iterable, Optional, Tuple

from nisystemlink.clients import tag as tbase
from typing_extensions import final


@final
class TagDataUpdate:
    """Contains information for updating parts of a tag's metadata on the server when
    used with the :meth:`TagManager.update()` method.

    The update can add keywords, add new properties, change the value of existing
    properties, modify the collect aggregates setting, and modify retention settings. To
    remove a keyword or property, pass the entire :class:`TagData` to the
    :meth:`TagManager.update()` method instead.
    """

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'TagDataUpdate' is not an acceptable base type")

    def __init__(
        self,
        path: str,
        data_type: tbase.DataType,
        keywords: Optional[Iterable[str]] = None,
        properties: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize an update of a tag's keywords and/or properties.

        Keywords and properties included in the update that are missing from the tag's
        metadata on the server are added, and properties that exist with a different
        value are replaced. At least one of ``keywords`` or ``properties`` must be
        specified.

        Args:
            path: The path of the tag to update.
            data_type: The data type of the tag to update.
            keywords: The list of keywords that will be added to the tag's metadata on
                the server, or None to not add any keywords.
            properties: The properties that will be added to or replaced in the tag's
                metadata on the server, or None to not modify any properties.

        Raises:
            ValueError: if ``path`` is None.
            ValueError: if both ``keywords`` and ``properties`` are None.
        """
        if path is None:
            raise ValueError("path cannot be None")
        self._path = path
        self._data_type = data_type

        if keywords is None and properties is None:
            raise ValueError(
                "Must specify at least one of keywords or properties to update"
            )
        self._keywords = list(keywords) if keywords is not None else None
        self._properties = None  # type: Optional[Dict[str, str]]
        if properties is not None:
            self._properties = dict(properties)

        self._collect_aggregates = None  # type: Optional[bool]

    @classmethod
    def from_tagdata(
        cls, data: tbase.TagData, fields: tbase.TagUpdateFields
    ) -> "TagDataUpdate":
        """Create an update by taking one or more fields from a :class:`TagData`.

        Args:
            data: The metadata to send to the server in the update.
            fields: One or more fields to include in the update.

        Raises:
            ValueError: if ``data`` is None.
            ValueError: if ``fields`` has no fields or invalid fields.
        """
        if data is None:
            raise ValueError("data cannot be None")

        if fields == 0:
            raise ValueError("Must specify at least one field to update")

        if (tbase.TagUpdateFields.ALL & fields) != fields:
            raise ValueError("Invalid field specified")

        obj = cls.__new__(cls)
        obj._path = data.path
        obj._data_type = data.data_type
        obj._keywords = None
        obj._properties = None
        obj._collect_aggregates = None

        if fields & tbase.TagUpdateFields.KEYWORDS and data.keywords:
            obj._keywords = list(data.keywords)

        if fields & tbase.TagUpdateFields.PROPERTIES and data.properties:
            obj._properties = dict(data.properties)
        if fields & tbase.TagUpdateFields.RETENTION:
            if obj._properties is None:
                obj._properties = {}
            data._copy_retention_properties(obj._properties)

        if fields & tbase.TagUpdateFields.COLLECT_AGGREGATES:
            obj._collect_aggregates = data.collect_aggregates

        return obj

    def to_json_dict(self) -> Dict[str, Any]:
        if self.data_type == tbase.DataType.UNKNOWN:
            raise ValueError("Invalid tag data type")

        data = {
            "path": tbase.TagPathUtilities.validate(self._path),
            "type": self._data_type.api_name,
        }  # type: Dict[str, Any]

        if self._keywords is not None:
            data["keywords"] = self._keywords
        if self._properties is not None:
            data["properties"] = self._properties
        if self._collect_aggregates is not None:
            data["collectAggregates"] = self._collect_aggregates
        return data

    @property
    def collect_aggregates(self) -> Optional[bool]:  # noqa: D401
        """The :attr:`TagData.collect_aggregates` setting to send with the update, or None to not send a value."""
        return self._collect_aggregates

    @property
    def data_type(self) -> tbase.DataType:  # noqa: D401
        """The data type for the tag's values."""
        return self._data_type

    @property
    def keywords(self) -> Optional[Tuple[str, ...]]:  # noqa: D401
        """The list of keywords to send with the update, or None to not send any keywords."""
        return tuple(self._keywords) if self._keywords is not None else None

    @property
    def path(self) -> str:  # noqa: D401
        """The tag's path, which uses a dot-separated hierarchy to uniquely identify the tag on the server."""
        return self._path

    @property
    def properties(self) -> Optional[Dict[str, str]]:  # noqa: D401
        """The properties send with the update, or None to not send any properties."""
        if self._properties:
            return dict(self._properties)
        else:
            return None
