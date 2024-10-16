"""Implementation of AuthClient."""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get

from . import models


class AuthClient(BaseClient):
    """Class contains a set of methods to access the APIs of SystemLink Auth Client."""

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
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, base_path="/niauth/v1/")

    @get("auth")
    def authenticate(self) -> models.AuthInfo:
        """Authenticates the given x-ni-api-key and returns information about the caller."""
        ...
