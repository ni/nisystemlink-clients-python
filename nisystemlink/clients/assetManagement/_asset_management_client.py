"""Implementation of AssetManagementClient."""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import (
    delete,
    get,
    post,
)
from uplink import Field, Header, Query

from . import models


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

    @get(
        "assets",
        args=[
            Query("skip"),
            Query("take"),
            Query("calibratableOnly"),
            Query("fileIngestionWorkspace"),
            Header("x-ni-api-key"),
        ],
    )
    def get_assets(
        self,
        skip: Optional[int] = None,
        take: Optional[int] = None,
        calibratableOnly: Optional[bool] = None,
        x_ni_api_key: Optional[str] = None,
    ) -> models.AssetsResponse:
        """Gets Assets.

        Args:
            skip: number of resources to skip in the result when paging.
            take: how many resources to return in the result, or -1 to use a default defined by the service.
            calibratableOnly: whether to generate a report with calibrated asset specific columns.
            x_ni_api_key: api key genreated by ni services.

        Returns:
            All Assets according to the given arguments.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @get("asset-summary")
    def get_asset_summary(self) -> models.AssetSummaryResponse:
        """Gets Assets Summary.

        Returns:
            Assets Summary of all assets.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @get("assets/{asset_id}")
    def get_asset_by_id(self, asset_id: str) -> models.Asset:
        """Gets an Asset with the given Id.

        Args:
            asset_id: Id of the asset to be retrieved

        Returns:
            Asset if an asset is present with the id.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @post("assets", args=[Field("assets")])
    def create_assets(
        self, assets: List[models.AssetCreate]
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

    @post("export-assets")
    def export_assets(
        self, export: models.ExportAssetsRequest
    ) -> models.ExportAssetsResponse:
        """Export Assets Report.

        Args:
            export: an export request containing information about export options.

        Returns:
            An object containing an array of file identifiers from the file ingestion service.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @post("update-assets", args=[Field("assets")])
    def update_assets(
        self, assets: List[models.AssetUpdate]
    ) -> models.UpdateAssetsPartialSuccessResponse:
        """Update Assets.

        Args:
            assets: an array of assets to update.

        Returns:
            Response object with array of updated assets and array of failed assets

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @post("assets/{asset_id}/history/query-location")
    def query_location(
        self, query: models.QueryLocationHistoryRequest, asset_id: str
    ) -> models.ConnectionHistoryResponse:
        """Query Asset Location History.

        Args:
            asset_id: Id of the Asset to retrieve location history about.
            query: an object containing options for querying history.
            x_ni_api_key: api key genreated by ni services.

        Returns:
            Response object containing an array of history items and a continuation token.

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

    @post("assets/{asset_id}/file", args=[Field("fileIds")])
    def link_files(
        self, fileIds: List[str], asset_id: str
    ) -> Optional[models.LinkFilesPartialSuccessResponse]:
        """Link files to Asset.

        Args:
            asset_id: Id of the asset to link the files to.
            files: an array of file ids to link to the asset.

        Returns:
            Response object containing an array of suceeded file ids and an array of failed file ids.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @delete("assets/{asset_id}/files/{file_id}")
    def unlink_files(self, asset_id: str, file_id: str) -> Optional[int]:
        """Unlink files from Asset.

        Args:
            asset_id: Id of the asset to unlink the file from.
            file_id: Id of the file to unlink the asset from.

        Returns:
            Status Code of the unlinking operation.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...
