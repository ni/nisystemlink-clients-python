# -*- coding: utf-8 -*-

"""Implementation of HttpConfigurationFile."""

from typing import Any, Dict, Optional

from typing_extensions import final


@final
class HttpConfigurationFile:
    """Represents a SystemLink HTTP configuration JSON file."""

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'HttpConfigurationFile' is not an acceptable base type")

    __slots__ = [
        "_id",
        "_display_name",
        "_connection_type",
        "_uri",
        "_api_key",
        "_cert_path",
    ]

    def __init__(self) -> None:
        self._id = None  # type: Optional[str]
        self._display_name = None  # type: Optional[str]
        self._connection_type = None  # type: Optional[str]
        self._uri = None  # type: Optional[str]
        self._api_key = None  # type: Optional[str]
        self._cert_path = None  # type: Optional[str]

    @staticmethod
    def from_json_dict(d: Dict[str, Any]) -> "HttpConfigurationFile":
        """Create from the dictionary format that is stored as JSON in the file."""
        self = HttpConfigurationFile()
        self.id = d.get("Id")
        self.display_name = d.get("DisplayName")
        self.connection_type = d.get("ConnectionType")
        self.uri = d.get("Uri")
        self.api_key = d.get("ApiKey")
        self.cert_path = d.get("CertPath")
        return self

    @property
    def id(self) -> Optional[str]:  # noqa: D401
        """The ID of this configuration."""
        return self._id

    @id.setter
    def id(self, value: Optional[str]) -> None:
        self._id = value

    @property
    def display_name(self) -> Optional[str]:  # noqa: D401
        """A user-friendly display name for this configuration."""
        return self._display_name

    @display_name.setter
    def display_name(self, value: Optional[str]) -> None:
        self._display_name = value

    @property
    def connection_type(self) -> Optional[str]:  # noqa: D401
        """The type of connection to use."""
        return self._connection_type

    @connection_type.setter
    def connection_type(self, value: Optional[str]) -> None:
        self._connection_type = value

    @property
    def uri(self) -> Optional[str]:  # noqa: D401
        """The URI of the SystemLink server."""
        return self._uri

    @uri.setter
    def uri(self, value: Optional[str]) -> None:
        self._uri = value

    @property
    def api_key(self) -> Optional[str]:  # noqa: D401
        """The API key of this client."""
        return self._api_key

    @api_key.setter
    def api_key(self, value: Optional[str]) -> None:
        self._api_key = value

    @property
    def cert_path(self) -> Optional[str]:  # noqa: D401
        """The path to the server's HTTPS certificate, relative to the Skyline Certificates directory."""
        return self._cert_path

    @cert_path.setter
    def cert_path(self, value: Optional[str]) -> None:
        self._cert_path = value
