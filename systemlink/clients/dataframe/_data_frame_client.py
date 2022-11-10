# TODO: Wrap Uplink decorators to add typing information
# mypy: disable-error-code = misc

"""Implementation of DataFrameClient."""

from typing import Optional

from systemlink.clients import core
from systemlink.clients.core._uplink._base_client import BaseClient
from uplink import get, returns


class DataFrameClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`core.JupyterHttpConfiguration` is used.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration)

    @returns.json()
    @get("nidataframe")
    # TODO: Create model class for return type
    def api_info(self) -> dict:
        """Returns information about API versions and available operations."""
        pass
