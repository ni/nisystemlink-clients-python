"""Implementation of WebappClient."""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post, response_handler
from nisystemlink.clients.core.helpers import IteratorFileLike
from requests.models import Response
from uplink import Body

from . import models


def _iter_content_filelike_wrapper(response: Response) -> IteratorFileLike:
    return IteratorFileLike(response.iter_content(chunk_size=4096))


class WebappClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

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
    def query_webapps(self, query: models.WebAppsAdvancedQuery) -> models.PagedWebApps:
        """Query webapps using dynamic LINQ formatted query.

        Args:
            query (models.WebAppsAdvancedQuery): The filter criteria for webapps, consisting of a
            string of queries composed using AND/OR operators.

        Returns:
            models.WebAppsQueryResult: Paged result of WebApps that match the query.

        Raises:
            ApiException: if unable to communicate with the WebApp Service
                or provided an invalid argument.
        """
        ...

    @response_handler(_iter_content_filelike_wrapper)
    @get("{id}/content")
    def get_content(self, id: str) -> IteratorFileLike:
        """Get the content of a webapp. ContentType varies from JSON for dashboards
        and templates or redirect to main HTML for WebVIs.

        Args:
            id (str): Webapp id to get the content of.

        Returns:
            A file-like object for reading the WebApp content.

        Raises:
            ApiException: if unable to communicate with the WebApp Service
                or provided an invalid id.
        """
        ...
