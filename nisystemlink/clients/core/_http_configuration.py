# -*- coding: utf-8 -*-

"""Implementation of HttpConfiguration."""

import pathlib
import urllib.parse
from typing import Dict, Optional


class HttpConfiguration:
    """Represents the configuration for accessing a SystemLink service over HTTP."""

    DEFAULT_TIMEOUT_MILLISECONDS = 60000
    """The default value of :attr:`timeout_milliseconds` to use when making API calls."""

    _SYSTEM_LINK_API_KEY_HEADER = "x-ni-api-key"

    def __init__(
        self,
        server_uri: str,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        cert_path: Optional[pathlib.Path] = None,
    ) -> None:
        """Initialize a configuration.

        If neither ``api_key`` nor ``username`` and ``password`` are set, the
        configuration will use anonymous access, and any API calls that require
        authorization will fail.

        Args:
            server_uri: The scheme, host, and port (if not default) of the web server
                hosting the SystemLink service to connect to. Additional Uri properties
                such as ``urllib.parse.urlparse().path`` and
                ``urllib.parse.urlparse().query`` are ignored.
            api_key: The API key to send with requests.
            username: The name of the user to use when authorization is required.
            password: The user's password to use when authorization is required.
            cert_path: Local path to an SSL certificate file.

        Raises:
            ValueError: if ``server_uri`` is missing scheme or host information.
            ValueError: if ``username`` or ``password`` is set, but not both.
        """
        uri = urllib.parse.urlsplit(server_uri)
        if not uri.scheme:
            raise ValueError(
                "Scheme (e.g. http) not included in server_uri: '{}'".format(uri)
            )
        if not uri.hostname:
            raise ValueError(
                "Host (e.g. foo.com) not included in server_uri: '{}'".format(uri)
            )
        self._server_uri = urllib.parse.urlunsplit(uri[:2] + ("", "", ""))

        self._api_keys = None  # type: Optional[Dict[str, str]]
        if api_key:
            self._api_keys = {self._SYSTEM_LINK_API_KEY_HEADER: api_key}
        elif username or password:
            if not username or not password:
                raise ValueError("If username or password is set, both must be set")
            self._username = username
            self._password = password

        self._cert_path = cert_path

        self._user_agent = ""  # type: Optional[str]

        self._timeout_ms = self.DEFAULT_TIMEOUT_MILLISECONDS

    @property
    def timeout_milliseconds(self) -> int:  # noqa: D401
        """The number of milliseconds before a request times out with an error.

        Changing the timeout will not affect APIs that have already read the
        configuration.
        """
        return self._timeout_ms

    @timeout_milliseconds.setter
    def timeout_milliseconds(self, value: int) -> None:
        self._timeout_ms = value

    @property
    def user_agent(self) -> Optional[str]:  # noqa: D401
        """The string to pass the web server as the product name or names making the
        request, or None to use a library-specific default.

        Changing the user-agent will not affect APIs that have already read the
        configuration.
        """
        return self._user_agent or None

    @user_agent.setter
    def user_agent(self, value: Optional[str]) -> None:
        self._user_agent = value

    @property
    def api_keys(self) -> Optional[Dict[str, str]]:  # noqa: D401
        """The available API keys to use for authorization, or None if none were provided."""
        return dict(self._api_keys) if self._api_keys else None

    @property
    def server_uri(self) -> str:  # noqa: D401
        """The ``urllib.parse.urlparse().scheme``, ``urllib.parse.urlparse().hostname``,
        and ``urllib.parse.urlparse().port`` of the web server hosting the SystemLink
        service to connect to.

        Additional Uri properties such as ``urllib.parse.urlparse().path`` and
        ``urllib.parse.urlparse().query`` are ignored.
        """
        return self._server_uri

    @property
    def username(self) -> Optional[str]:  # noqa: D401
        """The username to use for HTTP authentication, or None if none was provided."""
        return self._username

    @property
    def password(self) -> Optional[str]:  # noqa: D401
        """The password to use for HTTP authentication, or None if none was provided."""
        return self._password

    @property
    def cert_path(self) -> Optional[pathlib.Path]:
        """Local path to an SSL certificate file."""
        return self._cert_path
