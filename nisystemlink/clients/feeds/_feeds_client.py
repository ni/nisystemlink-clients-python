"""Implementation of SystemLink Feeds Client."""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
from uplink import Body, Part, Path, Query

from . import models


class FeedsClient(BaseClient):
    """Class contains a set of methods to access the APIs of SystemLink Feed Client."""

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>` # noqa: W505
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Feeds Service.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, base_path="/nifeed/v1/")

    @post("feeds")
    def create_feed(
        self, feed: models.CreateFeedRequest
    ) -> models.CreateOrUpdateFeedResponse:
        """Create a new feed with the provided feed details.

        Args:
            feeds (models.CreateFeedsRequest): Request model to create the feed.

        Returns:
            models.CreateorUpdateFeedsResponse: Feed details of the newly created feed.
        """
        ...

    @get("feeds", args=[Query, Query])
    def query_feeds(
        self,
        platform: Optional[str] = None,
        workspace: Optional[str] = None,
    ) -> models.FeedsQueryResponse:
        """Get a set of feeds based on the provided `platform` and `workspace`.

        Args:
            platform (Optional[str]): Information about system platform. Defaults to None.
            workspace (Optional[str]): Workspace id. Defaults to None.

        Returns:
            models.FeedsQueryResponse: List of feeds.
        """
        ...

    @post("feeds/{feedId}/packages", args=[Path(name="feedId"), Body])
    def upload_package(
        self,
        feed_id: str,
        package: Part,
        overwrite: bool = Query[bool](False, name="shouldOverwrite"),
    ) -> models.UploadPackageResponse:
        """Upload package to feeds.

        Args:
            feed_id (str): ID of the feed.
            package (Part): Package file as a form data.
                Example: `package=open(filename, "rb")`
            overwrite (bool): To overwrite the package if exists. Defaults to false. # noqa: W505

        Returns:
            models.UploadPackageResponse: Upload package response.
        """
        ...
