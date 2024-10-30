"""Implementation of SystemLink Feeds Client."""

from typing import BinaryIO, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from uplink import Part, Path, Query

from . import models


class FeedsClient(BaseClient):
    """A set of methods to access the APIs of SystemLink Feeds Client."""

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Feeds Service.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, base_path="/nifeed/v1/")

    @post("feeds")
    def create_feed(self, feed: models.CreateFeedRequest) -> models.Feed:
        """Create a new feed with the provided feed details.

        Args:
            feeds (models.CreateFeedsRequest): Request model to create the feed.

        Returns:
            models.Feed: Details of the created feed.
        """
        ...

    @get("feeds", args=[Query, Query])
    def __query_feeds(
        self,
        platform: Optional[str] = None,
        workspace: Optional[str] = None,
    ) -> models.QueryFeedsResponse:
        """Get a set of feeds based on the provided `platform` and `workspace`.

        Args:
            platform (Optional[str]): Information about system platform. Defaults to None.
            workspace (Optional[str]): Workspace id. Defaults to None.

        Returns:
            models.QueryFeedsResponse: List of feeds.
        """
        ...

    def query_feeds(
        self,
        platform: Optional[models.Platform] = None,
        workspace: Optional[str] = None,
    ) -> models.QueryFeedsResponse:
        """Get a set of feeds based on the provided `platform` and `workspace`.

        Args:
            platform (Optional[models.Platform]): Information about system platform. \
Defaults to None.
            workspace (Optional[str]): Workspace id. Defaults to None.

        Returns:
            models.QueryFeedsResponse: List of feeds.
        """
        platform_by_str = platform.value if platform is not None else None
        response = self.__query_feeds(
            platform=platform_by_str,
            workspace=workspace,
        )

        return response

    @post(
        "feeds/{feedId}/packages",
        args=[Path(name="feedId"), Query(name="ShouldOverwrite")],
    )
    def __upload_package(
        self,
        feed_id: str,
        package: Part,
        overwrite: Query = False,
    ) -> models.Package:
        """Upload package to SystemLink feed.

        Args:
            feed_id (str): ID of the feed.
            package (Part): Package file as a form data.
            overwrite (Query): Set to True, to overwrite the package if it already exists.\
Defaults to False.

        Returns:
            models.Package: Uploaded package response information.
        """
        ...

    def upload_package(
        self,
        feed_id: str,
        package: BinaryIO,
        overwrite: bool = False,
    ) -> models.Package:
        """Upload package to SystemLink feed.

        Args:
            feed_id (str): ID of the feed.
            package (BinaryIO): Package file to be uploaded.
            overwrite (bool): Set to True, to overwrite the package if it already exists.\
Defaults to False.

        Returns:
            models.Package: Uploaded package response information.
        """
        response = self.__upload_package(
            feed_id=feed_id,
            overwrite=overwrite,
            package=package,
        )

        return response

    @delete(
        "feeds/{feedId}",
        args=[Path(name="feedId")],
    )
    def delete_feed(self, id: str) -> None:
        """Delete feed and its packages.

        Args:
            id (str): ID of the feed to be deleted.

        Returns:
            None.
        """
        ...