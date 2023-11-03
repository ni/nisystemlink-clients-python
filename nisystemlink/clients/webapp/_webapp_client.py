"""Implementation of WebappClient."""

from typing import Any, Optional

from uplink import Body

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post

from . import models


class WebappClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """
        Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`JupyterHttpConfiguration <nisystemlink.clients.core.JupyterHttpConfiguration>`
                is used.

        Raises:
            ApiException: if unable to communicate with the WebApp Service.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, base_path="/niapp/v1/webapps/")

    @post("query", args=[Body])
    def query_webapps(
        self, query: models.WebAppsAdvancedQuery
    ) -> models.WebAppsResponse:
        """
        Use the Dynamic Linq query language to specify filters for webapps.
        An empty request body queries all webapps.
        """
        ...

    @get("{id}/content")
    def get_content(self, id: str) -> Any:
        """
        Get the content of a webapp. ContentType varies from JSON for dashboards
        and templates or redirect to main HTML for WebVIs.

        Args:
            id (str): Webapp id to get the content of.

        Returns:
            Any: Content of the Webapp
        """
        ...
