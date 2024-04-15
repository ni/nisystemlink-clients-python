"""Implementation of TestMonitor Client"""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post

from . import models


class TestMonitorClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration]):
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()
        super.__init__(configuration, base_path="/nitestmonitor/v2/")

    @get("")
    def api_info(self) -> models.V2Operations:
        """Get information about the available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the `nitestmonitor` service.
        """
        ...
