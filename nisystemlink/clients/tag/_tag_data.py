# -*- coding: utf-8 -*-

"""Implementation of TagData."""

from typing import Any, Dict, Iterable, List, Optional

from nisystemlink.clients import tag as tbase
from typing_extensions import final


@final
class TagData:
    """Contains the metadata for a SystemLink tag."""

    _RETENTION_TYPE_PROP = "nitagRetention"

    _RETENTION_TYPE_NONE = "NONE"

    _RETENTION_TYPE_DURATION = "DURATION"

    _RETENTION_TYPE_COUNT = "COUNT"

    _RETENTION_TYPE_PERMANENT = "PERMANENT"

    _HISTORY_TTL_DAYS_PROP = "nitagHistoryTTLDays"

    _MAX_HISTORY_COUNT_PROP = "nitagMaxHistoryCount"

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'TagData' is not an acceptable base type")

    def __init__(
        self,
        path: str,
        data_type: Optional[tbase.DataType] = None,
        keywords: Optional[Iterable[str]] = None,
        properties: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize an instance.

        Args:
            path: The tag's path, which uses a dot-separated hierarchy to uniquely
                identify the tag on the server.
            data_type: The data type for the tag's values.
            keywords: The tag's keywords.
            properties: The tag's properties.
        """
        self._path = path
        self._data_type = tbase.DataType.UNKNOWN if data_type is None else data_type
        self._keywords = list(keywords) if keywords else []
        self._properties = {}  # type: Dict[str, str]
        self._collect_aggregates = False
        self._retention_type = tbase.RetentionType.NONE
        self._retention_count = None  # type: Optional[int]
        self._retention_days = None  # type: Optional[int]
        if properties:
            self.replace_properties(properties)

    @classmethod
    def from_json_dict(cls, data: Dict[str, Any]) -> "TagData":
        data_type_str = data.get("type") or "UNKNOWN"
        data_type = tbase.DataType.from_api_name(data_type_str)
        tag = cls(data["path"], data_type, data.get("keywords"), data.get("properties"))
        if data.get("collectAggregates"):
            tag.collect_aggregates = True
        return tag

    def to_json_dict(self) -> Dict[str, Any]:
        self.validate_path()
        if self.data_type == tbase.DataType.UNKNOWN:
            raise ValueError("Invalid tag data type")

        data = {}  # type: Dict[str, Any]
        data["path"] = self._path
        data["type"] = self._data_type.api_name
        data["collectAggregates"] = self.collect_aggregates

        if self._keywords:
            data["keywords"] = self._keywords

        data["properties"] = dict(self._properties) if self._properties else {}
        self._copy_retention_properties(data["properties"])
        if not data["properties"]:
            del data["properties"]

        return data

    @property
    def collect_aggregates(self) -> bool:  # noqa: D401
        """Whether the server should keep aggregate information for the tag.

        The information collected depends on the tag's :attr:`data_type`.
        """
        return self._collect_aggregates

    @collect_aggregates.setter
    def collect_aggregates(self, value: bool) -> None:
        self._collect_aggregates = value

    @property
    def data_type(self) -> tbase.DataType:  # noqa: D401
        """The data type for the tag's values.

        Changing the data type of an existing tag requires deleting the tag and creating
        a new one of a different data type.
        """
        return self._data_type

    @data_type.setter
    def data_type(self, value: tbase.DataType) -> None:
        self._data_type = value

    @property
    def keywords(self) -> List[str]:  # noqa: D401
        """The list of keywords associated with the tag."""
        return self._keywords

    @property
    def path(self) -> str:  # noqa: D401
        """The tag's path, which uses a dot-separated hierarchy to uniquely identify the tag on the server."""
        return self._path

    @property
    def properties(self) -> Dict[str, str]:  # noqa: D401
        """The properties associated with the tag."""
        return self._properties

    @property
    def retention_type(self) -> tbase.RetentionType:  # noqa: D401
        """How the tag's historical values are retained by the tag historian, if available.

        The :attr:`retention_count` and :attr:`retention_days` properties can further
        customize when values are removed from the historian.

        The tag historian is an optional component for SystemLink Server installations,
        and is not available in SystemLink Cloud. The tag's historical values are not
        retained when the tag historian is not available, regardless of the retention
        type.
        """
        return self._retention_type

    @retention_type.setter
    def retention_type(self, value: tbase.RetentionType) -> None:
        self._retention_type = value

    @property
    def retention_count(self) -> Optional[int]:  # noqa: D401
        """The number of historical values to retain when :attr:`retention_type` is
        :attr:`RetentionType.COUNT`, or None to use the server-specified default of
        10000.
        """
        return self._retention_count

    @retention_count.setter
    def retention_count(self, value: Optional[int]) -> None:
        self._retention_count = value

    @property
    def retention_days(self) -> Optional[int]:  # noqa: D401
        """The number of days to keep a tag's historical values when
        :attr:`retention_type` is :attr:`RetentionType.DURATION`, or None to use the
        server-specified default of 30 days.
        """
        return self._retention_days

    @retention_days.setter
    def retention_days(self, value: Optional[int]) -> None:
        self._retention_days = value

    def replace_keywords(self, keywords: Iterable[str]) -> None:
        """Replace all of the tag's :attr:`keywords` with those in ``keywords``.

        Args:
            keywords: The tag's new keywords, or None to clear all keywords.
        """
        self._keywords[:] = keywords

    def replace_properties(self, properties: Dict[str, str]) -> None:
        """Replace all of the tag's :attr:`properties` with those in ``properties``.

        Args:
            properties: The tag's new properties, or None to clear all properties.
        """
        self._properties.clear()

        if properties is None:
            return

        for key, value in properties.items():
            # Check for special properties to parse.
            if key == self._RETENTION_TYPE_PROP:
                if value == self._RETENTION_TYPE_COUNT:
                    self._retention_type = tbase.RetentionType.COUNT
                elif value == self._RETENTION_TYPE_DURATION:
                    self._retention_type = tbase.RetentionType.DURATION
                elif value == self._RETENTION_TYPE_NONE:
                    self._retention_type = tbase.RetentionType.NONE
                elif value == self._RETENTION_TYPE_PERMANENT:
                    self._retention_type = tbase.RetentionType.PERMANENT
                else:
                    self._retention_type = tbase.RetentionType.INVALID
            elif key == self._HISTORY_TTL_DAYS_PROP:
                try:
                    self._retention_days = int(value)
                except ValueError:
                    self._retention_days = None
            elif key == self._MAX_HISTORY_COUNT_PROP:
                try:
                    self._retention_count = int(value)
                except ValueError:
                    self._retention_count = None
            else:
                # Not a special property. Preserve it in the dictionary.
                self._properties[key] = value

    def _copy_retention_properties(self, destination: Dict[str, str]) -> None:
        """Copy the tag's retention settings into ``destination``.

        Clients do not typically call this method directly.

        Args:
            destination: The dictionary to copy into. Existing properties with names in
                common with the retention properties will be overwritten.

        Raises:
            ValueError: if ``destination`` is None.
        """
        if destination is None:
            raise ValueError("destination cannot be None")

        if self._retention_type == tbase.RetentionType.NONE:
            destination[self._RETENTION_TYPE_PROP] = self._RETENTION_TYPE_NONE
        elif self._retention_type == tbase.RetentionType.DURATION:
            destination[self._RETENTION_TYPE_PROP] = self._RETENTION_TYPE_DURATION
        elif self._retention_type == tbase.RetentionType.COUNT:
            destination[self._RETENTION_TYPE_PROP] = self._RETENTION_TYPE_COUNT
        elif self._retention_type == tbase.RetentionType.PERMANENT:
            destination[self._RETENTION_TYPE_PROP] = self._RETENTION_TYPE_PERMANENT

        if self._retention_count is not None:
            destination[self._MAX_HISTORY_COUNT_PROP] = str(self._retention_count)

        if self._retention_days is not None:
            destination[self._HISTORY_TTL_DAYS_PROP] = str(self._retention_days)

    def clear_retention(self) -> None:
        """Clear all retention settings, setting it to use a
        :attr:`TagData.retention_type` of :attr:`RetentionType.NONE`.

        Args:
            tag: The tag whose retention will be cleared.
        """
        self.retention_type = tbase.RetentionType.NONE
        self.retention_count = None
        self.retention_days = None

    def set_retention_count(self, count: int) -> None:
        """Set the number of historical values to retain.

        Args:
            count: The number of historical values to retain.
        """
        self.retention_type = tbase.RetentionType.COUNT
        self.retention_count = count
        self.retention_days = None

    def set_retention_days(self, days: int) -> None:
        """Set the historical values to be retained for the specified number of days.

        Args:
            days: The number of days a historical value will be kept.
        """
        self.retention_type = tbase.RetentionType.DURATION
        self.retention_count = None
        self.retention_days = days

    def validate_type(self, required_type: tbase.DataType) -> None:
        """Validate that the tag's data type matches ``required_type``.

        Clients do not typically call this method directly.

        Args:
            required_type: The data type required by the API.

        Raises:
            ValueError: if this is not a tag of the required type with a valid path.
            ValueError: if ``required_type`` is :attr:`DataType.UNKNOWN`.
        """
        if required_type == tbase.DataType.UNKNOWN:
            raise ValueError("required_type is not a valid data type")

        if self.data_type != required_type:
            raise ValueError(
                "Tag must be a {} type but is a {} tag".format(
                    required_type.name, self.data_type.name
                )
            )

    def validate_path(self) -> str:
        """Validate the path as an input and returns it.

        Clients do not typically call this method directly.

        Returns:
            The validated path.

        Raises:
            ValueError: if the tag's path is invalid.
        """
        if self.path is None:
            raise ValueError("Tag path cannot be None")

        return tbase.TagPathUtilities.validate(self.path)
