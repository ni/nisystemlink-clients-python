"""Implementation of AuthClient."""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get

from . import models


class AuthClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`JupyterHttpConfiguration <nisystemlink.clients.core.JupyterHttpConfiguration>` # noqa: W505
                is used.

        Raises:
            ApiException: if unable to communicate with the Auth Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/niauth/v1/")

    @get("auth")
    def get_auth_info(self) -> models.AuthInfo:
        """Gets information about the authenticated API Key."""
        ...
