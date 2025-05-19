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
            ApiException: if unable to communicate with the AssetManagement Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/niapm/v1/")

    @post("assets", args=[Field("assets")])
    def create_assets(
        self, assets: List[models.AssetCreateRequest]
    ) -> models.AssetsCreatePartialSuccessResponse:
        """Create Assets.

        Args:
            assets: an array of assets that should be created.

        Returns:
            Response object with array of created assets and array of failed assets.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @post("query-assets")
    def query_assets(self, query: models.QueryAssetRequest) -> models.AssetsResponse:
        """Query Assets.

        Args:
            query: an object containing filters to apply when retrieving assets.

        Returns:
            Assets Response containing the assets satisfying the query and the total count of matching assets.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @post("delete-assets", args=[Field("ids")])
    def delete_assets(self, ids: List[str]) -> models.DeleteAssetsResponse:
        """Delete Assets.
        Args:
            assets: an arry of IDs of the assets to delete all information for.
        Returns:
            Response object containing the ids of the assets which were deleted.
        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...
