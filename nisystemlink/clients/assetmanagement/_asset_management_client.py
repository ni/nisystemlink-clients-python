"""Implementation of AssetManagementClient."""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import post
from uplink import Field, retry

from . import models


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class AssetManagementClient(BaseClient):
    def __init__(self, configuration: Optional[HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: If unable to communicate with the AssetManagement Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/niapm/v1/")

    @post("assets", args=[Field("assets")])
    def create_assets(
        self, assets: List[models.CreateAssetRequest]
    ) -> models.CreateAssetsPartialSuccessResponse:
        """Create Assets.

        Args:
            assets: Array of assets that should be created.

        Returns:
            AssetsCreatePartialSuccessResponse: Array of created assets and array of failed.

        Raises:
            ApiException: If unable to communicate with the `asset management` service or if there are invalid
            arguments.
        """
        ...

    @post("query-assets")
    def query_assets(
        self, query: models.QueryAssetsRequest
    ) -> models.QueryAssetsResponse:
        """Query Assets.

        Args:
            query: Object containing filters to apply when retrieving assets.

        Returns:
            AssetsResponse: Assets Response containing the assets satisfying the query and
            the total count of matching assets.

        Raises:
            ApiException: If unable to communicate with the `asset management` service or if there are invalid
            arguments.
        """
        ...

    @post("delete-assets", args=[Field("ids")])
    def delete_assets(self, ids: List[str]) -> models.DeleteAssetsResponse:
        """Delete Assets.

        Args:
            assets: Arry of IDs of the assets to delete all information for.

        Returns:
            DeleteAssetsResponse: Response Object containing the ids of the assets which were deleted.

        Raises:
            ApiException: If unable to communicate with the `asset management` service or if there are invalid
            arguments.
        """
        ...
