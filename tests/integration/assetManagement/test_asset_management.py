from typing import List
from xmlrpc.client import DateTime
from nisystemlink.clients.core._uplink import _json_model
import pytest
from nisystemlink.clients.assetManagement import AssetManagementClient
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.assetManagement.models import (
    Asset,
    AssetsResponse,
    CreateAssetsRequest,
    AssetsCreatePartialSuccessResponse,
    DeleteAssetsRequest,
    DeleteAssetsResponse,
    AssetSummaryResponse,
    QueryAssetRequest,
    ExportAssetsRequest,
    ExportAssetsResponse,
    UpdateAssetsRequest,
    UpdateAssetsPartialSuccessResponse,
    QueryLocationHistoryRequest,
    ConnectionHistoryResponse,
    LinkFilesRequest,
    LinkFilesPartialSuccessResponse,
    NoContentResult
)
from nisystemlink.clients.assetManagement.models._asset_create import (
    AssetCreate
)
from nisystemlink.clients.assetManagement.models._asset import (
    AssetBusType,
    AssetType,
    AssetDiscoveryType,
    SelfCalibration,
    AssetLocation,
    AssetPresenceWithSystemConnection,
    AssetPresence,
    ExternalCalibration
)
from nisystemlink.clients.assetManagement.models._export_assets import (
    ResponseFormat,
    Destination
)
from nisystemlink.clients.assetManagement.models._asset_update import (
    AssetUpdate
)
from nisystemlink.clients.assetManagement.models._query_location import (
    ResponseFormat as LocationResponseFormat,
    Destination as LocationDestination
)

@pytest.fixture(scope="class")
def create_assets_request() -> CreateAssetsRequest:
    createAssetRequest = CreateAssetsRequest(
        assets = [
            AssetCreate(
                bus_type = AssetBusType.ACCESSORY,
                asset_type = AssetType.DEVICE_UNDER_TEST,
                discovery_type = AssetDiscoveryType.AUTOMATIC,
                self_calibration = SelfCalibration(date = "hh:mm:ss"),
                is_ni_asset = True,
                location = AssetLocation(state = AssetPresenceWithSystemConnection(asset_presence = AssetPresence.PRESENT)),
                external_calibration = ExternalCalibration(
                    date = "hh:mm:ss",
                    recommended_interval = 10,
                    next_recommended_date = "hh:mm:ss",
                    next_custom_due_date = "hh:mm:ss",
                    resolved_due_date = "hh:mm:ss"
                ),
            )
        ]
    )
    
    return create_assets_request

@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> AssetManagementClient:
    """Fixture to create a AssetManagementClient instance"""
    return AssetManagementClient(enterprise_config)

@pytest.mark.integration
@pytest.mark.enterprise
class TestAssetManagement:

    @pytest.mark.skip
    def test__get_assets__returns_all_assets(
        self, client: AssetManagementClient, create_assets_request
    ):
        response: AssetsResponse = client.get_assets()

        assert response is not None
        assert response.total_count > 0
        assert len(response.assets) > 0

    @pytest.mark.skip
    def test__get_assets_with_specific_take_value__returns_specific_number_of_assets(
        self, client: AssetManagementClient
    ):
        response: AssetsResponse = client.get_assets(take=10)

        assert response is not None
        assert response.total_count > 0
        assert len(response.assets) == 10

    @pytest.mark.skip
    def test__get_assets_summary__returs_assets_summary(
        self, client: AssetManagementClient
    ):
        response: AssetSummaryResponse = client.get_asset_summary()

        assert response is not None
        assert response.total > 0
        assert response.total == response.active + response.not_active

    @pytest.mark.skip
    def test__get_asset_by_correct_id__returns_the_asset(
        self, client: AssetManagementClient, create_assets_request
    ):
        asset_create_response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        asset_id = asset_create_response.assets[0].id
        response : Asset = client.get_asset_by_id(asset_id=asset_id)

        assert response is not None
        assert response == asset_create_response.assets[0]

        client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

    @pytest.mark.skip
    def test__get_asset_by_incorrect_id__does_not_return_the_asset(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"

        response = client.get_asset_by_id(asset_id=asset_id)

        response is None


    def test__create_one_asset__one_asset_gets_created(
        self, client: AssetManagementClient, create_assets_request
    ):
        response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        assert len(response.assets) == 1
        assert len(response.failed) == 0
        assert response.assets[0].model_number == 1
        assert response.assets[0].vendor_number == 2

        client.delete_assets(assets=DeleteAssetsRequest(ids=[response.assets[0].id]))

    @pytest.mark.skip
    def test__create_multiple_assets__all_succeed(
        self, client: AssetManagementClient, create_assets
    ):
        createAssetsRequest = CreateAssetsRequest(assets = [])
        for i in range(1,3):
            createAssetsRequest.assets.append(
                Asset(
                    model_number = i,
                    vendor_number = 2,
                    bus_type = AssetBusType.ACCESSORY,
                    asset_type = AssetType.DEVICE_UNDER_TEST,
                    discovery_type = AssetDiscoveryType.AUTOMATIC,
                    supports_self_calibration = True,
                    supports_external_calibration = True,
                    self_calibration = SelfCalibration(date = "hh:mm:ss"),
                    is_ni_asset = True,
                    location = AssetLocation(state = AssetPresenceWithSystemConnection(asset_presence = AssetPresence.PRESENT)),
                    is_system_controller = True,
                    external_calibration = ExternalCalibration(
                        date = "hh:mm:ss",
                        recommended_interval = 10,
                        next_recommended_date = "hh:mm:ss",
                        next_custom_date = "hh:mm:ss",
                        resolved_due_date = "hh:mm:ss"
                    ),
                    last_updated_timestamp = "hh:mm:ss",
                    supports_self_test = True,
                    supports_reset = True
                )
            )

        response: AssetsCreatePartialSuccessResponse = create_assets(createAssetsRequest)
        
        assert len(response.assets) == 2
        assert len(response.failed) == 0
        assert response.assets[0].model_number == 1
        assert response.assets[1].model_number == 2

    @pytest.mark.skip
    def test__query_assets_with_correct_id__returns_assets(
        self, client: AssetManagementClient, create_assets_request
    ):
        create_assets_response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        asset_id = create_assets_response.assets[0].id
        query_assets_request = QueryAssetRequest(
            ids = [asset_id],
            skip = 0,
            take = 1,
            descending = False,
            calibratable_only = False
        )

        response: AssetsResponse = client.query_assets(query=query_assets_request)

        assert response is not None
        assert response.assets[0] == create_assets_response.assets[0]

        client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

    @pytest.mark.skip
    def test__query_assets_with_incorrect_id__does_not_return_assets(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"
        query_assets_request = QueryAssetRequest(
            ids = [asset_id],
            skip = 0,
            take = 1,
            descending = False,
            calibratable_only = False
        )

        response = client.query_assets(query=query_assets_request)

        assert response is None
        assert len(response.assets) == 0

    @pytest.mark.skip
    def test__export_assets__returns_file_ids(
        self, client: AssetManagementClient
    ):
        request = ExportAssetsRequest(
            response_format = ResponseFormat.CSV,
            destination = Destination.FILE_SERVICE
        )

        response: ExportAssetsResponse = client.export_assets(export=request)

        assert response is not None
        assert (response.file_id) > 0

    @pytest.mark.skip
    def test__update_assets_with_correct_id__updates_assets(
        self, client: AssetManagementClient, create_assets_request
    ):
        create_assets_response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        asset_id = create_assets_response.assets[0].id

        update_asset_request = UpdateAssetsRequest(
            assets = [
                AssetUpdate(
                    model_number = 1,
                    vendor_number = 2,
                    bus_type = AssetBusType.FIRE_WIRE,
                    asset_type = AssetType.DEVICE_UNDER_TEST,
                    supports_self_calibration = True,
                    supports_external_calibration = True,
                    self_calibration = SelfCalibration(date = "hh:mm:ss"),
                    is_ni_asset = True,
                    location = AssetLocation(state = AssetPresenceWithSystemConnection(asset_presence = AssetPresence.PRESENT)),
                    external_calibration = ExternalCalibration(
                        date = "hh:mm:ss",
                        recommended_interval = 10,
                        next_recommended_date = "hh:mm:ss",
                        next_custom_date = "hh:mm:ss",
                        resolved_due_date = "hh:mm:ss"
                    ),
                    properties = {"property-key": "property-value"},
                    supports_self_test = True,
                    supports_reset = True,
                    id = asset_id
                )
            ]
        )

        response: UpdateAssetsPartialSuccessResponse = client.update_assets(assets=update_asset_request)

        assert response is not None
        assert response.assets[0].bus_type == AssetBusType.FIRE_WIRE
        assert len(response.failed) == 0

        client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

    @pytest.mark.skip
    def test__update_assets_with_incorrect_id__does_not_update_assets(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"
        update_asset_request = UpdateAssetsRequest(
            assets = [
                AssetUpdate(
                    model_number = 1,
                    vendor_number = 2,
                    bus_type = AssetBusType.FIRE_WIRE,
                    asset_type = AssetType.DEVICE_UNDER_TEST,
                    supports_self_calibration = True,
                    supports_external_calibration = True,
                    self_calibration = SelfCalibration(date = "hh:mm:ss"),
                    is_ni_asset = True,
                    location = AssetLocation(state = AssetPresenceWithSystemConnection(asset_presence = AssetPresence.PRESENT)),
                    external_calibration = ExternalCalibration(
                        date = "hh:mm:ss",
                        recommended_interval = 10,
                        next_recommended_date = "hh:mm:ss",
                        next_custom_date = "hh:mm:ss",
                        resolved_due_date = "hh:mm:ss"
                    ),
                    properties = {"property-key": "property-value"},
                    supports_self_test = True,
                    supports_reset = True,
                    id = asset_id
                )
            ]
        )

        response: UpdateAssetsPartialSuccessResponse = client.update_assets(assets=update_asset_request)

        assert response is not None
        assert len(response.assets) == 0
        assert len(response.failed) == 1

    @pytest.mark.skip
    def test__query_location_with_correct_id__returns_location_history(
        self, client: AssetManagementClient, create_assets_request
    ):
        create_assets_response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        asset_id = create_assets_response.assets[0].id
        query_location_request = QueryLocationHistoryRequest(
            response_format = LocationResponseFormat.JSON,
            destination = LocationDestination.FILE_SERVICE
        )

        response: ConnectionHistoryResponse = client.query_location(asset_id=asset_id, query=query_location_request)

        assert response is not None
        assert len(response.history_items) > 0

        client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

    @pytest.mark.skip
    def test__query_location_with_incorrect_id__does_not_return_location_history(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"
        query_location_request = QueryLocationHistoryRequest(
            response_format = LocationResponseFormat.JSON,
            destination = LocationDestination.FILE_SERVICE
        )

        response: ConnectionHistoryResponse = client.query_location(asset_id=asset_id, query=query_location_request)

        assert response is not None
        assert len(response.history_items) == 0

    @pytest.mark.skip
    def test__delete_assets_with_Correct_id__deletes_assets(
        self, client: AssetManagementClient, create_assets_request
    ):
        create_assets_response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        asset_id = create_assets_response.assets[0].id

        response: DeleteAssetsResponse = client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

        assert response is not None
        assert response.ids[0] == asset_id

    @pytest.mark.skip
    def test__delete_assets_with_incorrect_id__fails(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect"

        response: DeleteAssetsResponse = client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

        assert response is not None
        assert len(response.ids) == 0
        assert len(response.failed) == 1

    @pytest.mark.skip
    def test__link_files_with_correct_asset_id__links_files(
        self, client: AssetManagementClient, create_assets_request
    ):
        create_assets_response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        asset_id = create_assets_response.assets[0].id
        file_ids = ["608a5684800e325b48837c2a"]

        response: LinkFilesPartialSuccessResponse = client.link_files(asset_id=asset_id, files=LinkFilesRequest(file_ids=file_ids))

        assert response is not None
        assert response.succeeded[0] == file_ids[0]
        assert len(response.failed) == 0

        client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

    @pytest.mark.skip
    def test__link_files_with_incorrect_asset_id__does_not_link_files(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"
        file_ids = ["608a5684800e325b48837c2a"]

        response: LinkFilesPartialSuccessResponse = client.link_files(asset_id=asset_id, files=LinkFilesRequest(file_ids=file_ids))

        assert response is not None
        assert len(response.succeeded) == 0
        assert response.failed[0] == file_ids[0]

    @pytest.mark.skip
    def test__unlink_files_with_correct_asset_id__unlinks_files(
        self, client: AssetManagementClient, create_assets_request
    ):
        create_assets_response: AssetsCreatePartialSuccessResponse = client.create_assets(assets=create_assets_request)
        asset_id = create_assets_response.assets[0].id

        response: NoContentResult = client.unlink_files(asset_id=asset_id, file_id="608a5684800e325b48837c2a")

        assert response is not None
        assert response.status_code == 0

        client.delete_assets(assets=DeleteAssetsRequest(ids=[asset_id]))

    @pytest.mark.skip
    def test__unlink_files_with_incorrect_asset_id__does_not_unlink_files(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"

        response: NoContentResult = client.unlink_files(asset_id=asset_id, file_id="608a5684800e325b48837c2a")

        assert response is not None
        assert response.status_code != 0