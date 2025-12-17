"""Implementation of AssetManagementClient."""

from datetime import datetime
from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.assetmanagement.models._update_utilization_request import (
    _UpdateUtilizationRequest,
)
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
    def __init__(self, configuration: HttpConfiguration | None = None):
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

        query_request = models._QueryAssetsRequest(**query_params)  # type: ignore

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
    ) -> models.LinkFilesPartialSuccessResponse | None:
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

    @post("query-asset-utilization-history")
    def query_asset_utilization_history(
        self, request: models.QueryAssetUtilizationHistoryRequest
    ) -> models.AssetUtilizationHistoryResponse:
        """Query asset utilization history.

        Args:
            request: Object containing filters for asset utilization and assets, including
                    utilization_filter, asset_filter, date range, and pagination options.

        Returns:
            AssetUtilizationHistoryResponse: Response containing the list of asset utilization
            history records that match the query, along with optional continuation token for pagination.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid arguments.
        """
        ...

    @post("assets/start-utilization")
    def start_utilization(
        self, request: models.StartUtilizationRequest
    ) -> models.StartUtilizationPartialSuccessResponse:
        """Start asset utilization tracking.

        Args:
            request: Object containing the utilization identifier, minion ID, asset identifications,
                    utilization category, task name, user name, and utilization timestamp.

        Returns:
            StartUtilizationPartialSuccessResponse: Response containing arrays of assets that successfully
            started utilization and those that failed, along with error information if any failures occurred.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid arguments.
        """
        ...

    @post("assets/end-utilization")
    def __end_utilization(
        self, request: _UpdateUtilizationRequest
    ) -> models.UpdateUtilizationPartialSuccessResponse:
        """End asset utilization tracking.

        Args:
            request: The request object containing utilization identifiers and timestamp.

        Returns:
            UpdateUtilizationPartialSuccessResponse: Response containing updated utilization IDs.
        """
        ...

    def end_utilization(
        self,
        ids: List[str],
        timestamp: Optional[datetime] = None,
    ) -> models.UpdateUtilizationPartialSuccessResponse:
        """End asset utilization tracking.

        Args:
            ids: Array of utilization identifiers representing the unique identifier
                of asset utilization history records to end.
            timestamp: The timestamp to use when ending the utilization.
                If not provided, the current server time will be used.

        Returns:
            UpdateUtilizationPartialSuccessResponse: Response containing arrays of utilization IDs that were
            successfully updated and those that failed, along with error information if any failures occurred.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid arguments.
        """
        request = _UpdateUtilizationRequest(
            utilization_identifiers=ids,
            utilization_timestamp=timestamp,
        )
        return self.__end_utilization(request)

    @post("assets/utilization-heartbeat")
    def __utilization_heartbeat(
        self, request: _UpdateUtilizationRequest
    ) -> models.UpdateUtilizationPartialSuccessResponse:
        """Send utilization heartbeat.

        Args:
            request: The request object containing utilization identifiers and timestamp.

        Returns:
            UpdateUtilizationPartialSuccessResponse: Response containing updated utilization IDs.
        """
        ...

    def utilization_heartbeat(
        self,
        ids: List[str],
        timestamp: Optional[datetime] = None,
    ) -> models.UpdateUtilizationPartialSuccessResponse:
        """Send utilization heartbeat to update asset utilization tracking.

        Args:
            ids: Array of utilization identifiers representing the unique identifier
                of asset utilization history records to update.
            timestamp: The timestamp to use for the heartbeat.
                If not provided, the current server time will be used.

        Returns:
            UpdateUtilizationPartialSuccessResponse: Response containing arrays of utilization IDs that were
            successfully updated and those that failed, along with error information if any failures occurred.

        Raises:
            ApiException: If unable to communicate with the asset management service or if there are invalid arguments.
        """
        request = _UpdateUtilizationRequest(
            utilization_identifiers=ids,
            utilization_timestamp=timestamp,
        )
        return self.__utilization_heartbeat(request)
