"""Implementation of AssetManagementClient."""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import post
from uplink import Field, Path, retry

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
            ApiException: If unable to communicate with the asset management Service.
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
            CreateAssetsPartialSuccessResponse: Array of created assets and array of failed.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid
            arguments.
        """
        ...

    @post("query-assets")
    def __query_assets(
        self, query: models._QueryAssetsRequest
    ) -> models.QueryAssetsResponse:
        """Query Assets.

        Args:
            query: Object containing filters to apply when retrieving assets.

        Returns:
            QueryAssetsResponse: Assets Response containing the assets satisfying the query and
            the total count of matching assets.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid
            arguments.
        """
        ...

    def query_assets(
        self, query: models.QueryAssetsRequest
    ) -> models.QueryAssetsResponse:
        """Query Assets.

        Args:
            query: Object containing filters to apply when retrieving assets.

        Returns:
            QueryAssetsResponse: Assets Response containing the assets satisfying the query and
            the total count of matching assets.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid
            arguments.
        """
        projection_str = (
            f"new({', '.join(projection.name for projection in query.projection)})"
            if query.projection
            else None
        )
        query_params = {
            "filter": query.filter,
            "take": query.take,
            "skip": query.skip,
            "return_count": query.return_count,
            "order_by": query.order_by,
            "descending": query.descending,
            "projection": projection_str,
        }

        query_params = {k: v for k, v in query_params.items() if v is not None}

        query_request = models._QueryAssetsRequest(**query_params)

        return self.__query_assets(query=query_request)

    @post("delete-assets", args=[Field("ids")])
    def delete_assets(self, ids: List[str]) -> models.DeleteAssetsResponse:
        """Delete Assets.

        Args:
            ids: List of IDs of the assets to delete.

        Returns:
            DeleteAssetsResponse: Response containing the IDs of the assets that were deleted.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid arguments.
        """
        ...

    @post("assets/{assetId}/file", args=[Path("assetId"), Field("fileIds")])
    def link_files(
        self, asset_id: str, file_ids: List[str]
    ) -> Optional[models.LinkFilesPartialSuccessResponse]:
        """Link files to an asset.

        Args:
            asset_id: The ID of the asset to which files should be linked.
            file_ids: The list of file IDs to link.

        Returns:
            None if all link files succeed, otherwise a response containing the IDs of files that were
            successfully linked and those that failed.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid arguments.
        """
        ...
