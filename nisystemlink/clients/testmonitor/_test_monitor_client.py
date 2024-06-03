"""Implementation of TestMonitor Client"""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get

from . import models
from uplink import Path, Query


class TestMonitorClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration]):
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()
        super().__init__(configuration, base_path="/nitestmonitor/v2/")

    @get("")
    def api_info(self) -> models.ApiInfo:
        """Get information about the available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the `nitestmonitor` service.
        """
        ...

    @get(
        "products",
        args=[Query("continuationToken"), Query("take"), Query("returnCount")],
    )
    def get_products(
        self,
        continuation_token: Optional[str] = None,
        take: Optional[int] = None,
        return_count: Optional[bool] = None,
    ) -> models.PagedProducts:
        """Reads a list of products.

        Args:
            continuation_token: The token used to paginate results.
            take: The number of products to get in this request.
            return_count: Whether or not to return the total number of products available.

        Returns:
            A list of products.

        Raises:
            ApiException: if unable to communicate with the TestMonitor Service
                or provided an invalid argument.
        """
        ...
