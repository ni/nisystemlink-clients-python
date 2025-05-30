from typing import List

import pytest
from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    Asset,
    AssetBusType,
    AssetDiscoveryType,
    AssetField,
    AssetLocationForCreate,
    AssetPresence,
    AssetPresenceStatus,
    AssetType,
    CreateAssetRequest,
    CreateAssetsPartialSuccessResponse,
    ExternalCalibration,
    QueryAssetsRequest,
    QueryAssetsResponse,
    SelfCalibration,
    TemperatureSensor,
)
from nisystemlink.clients.core._api_exception import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture
def create_asset(client: AssetManagementClient):
    """Fixture to return a factory that creates assets."""
    responses: List[CreateAssetsPartialSuccessResponse] = []

    def _create_assets(
        new_assets: List[CreateAssetRequest],
    ) -> CreateAssetsPartialSuccessResponse:
        response = client.create_assets(assets=new_assets)
        responses.append(response)
        return response

    yield _create_assets

    created_assets: List[Asset] = []
    for response in responses:
        if response.assets:
            created_assets = created_assets + response.assets
    client.delete_assets(
        ids=[asset.id for asset in created_assets if asset.id is not None]
    )


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> AssetManagementClient:
    """Fixture to create a AssetManagementClient instance"""
    return AssetManagementClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestAssetManagement:
    _workspace = "2300760d-38c4-48a1-9acb-800260812337"
    """Used the main-test default workspace since the client
    for creating a workspace has not been added yet"""

    _create_assets_request = [
        CreateAssetRequest(
            model_name="python integration test 1",
            serial_number="01BB8",
            vendor_name="NI",
            vendor_number="4244",
            bus_type=AssetBusType.ACCESSORY,
            name="Python Integration Tests 1",
            asset_type=AssetType.DEVICE_UNDER_TEST,
            firmware_version="A1",
            hardware_version="12A",
            visa_resource_name="vs-3144",
            temperature_sensors=[TemperatureSensor(name="Sensor0", reading=25.8)],
            supports_self_calibration=True,
            supports_external_calibration=True,
            custom_calibration_interval=24,
            self_calibration=SelfCalibration(
                temperature_sensors=[TemperatureSensor(name="Sensor0", reading=25.8)],
                is_limited=False,
                date="2022-06-07T18:58:05.000Z",
            ),
            is_NI_asset=True,
            workspace=_workspace,
            location=AssetLocationForCreate(
                state=AssetPresence(asset_presence=AssetPresenceStatus.PRESENT)
            ),
            external_calibration=ExternalCalibration(
                temperature_sensors=[TemperatureSensor(name="Sensor0", reading=25.8)],
                date="2022-06-07T18:58:05.000Z",
                recommended_interval=10,
                next_recommended_date="2023-11-14T20:42:11.583Z",
                next_custom_due_date="2024-11-14T20:42:11.583Z",
                resolved_due_date="2022-06-07T18:58:05.000Z",
            ),
            properties={"Key1": "Value1"},
            keywords=["Keyword1"],
            discovery_type=AssetDiscoveryType.AUTOMATIC,
            file_ids=["608a5684800e325b48837c2a"],
            supports_self_test=True,
            supports_reset=True,
            partNumber="A1234",
        )
    ]
    """CreateAssetRequest object"""

    def test__create_asset__returns_created_asset(
        self, client: AssetManagementClient, create_asset
    ):
        self._create_assets_request[0].model_number = 101
        create_response = create_asset(self._create_assets_request)

        asset_id = (
            create_response.assets[0].id
            if create_response.assets and create_response.assets[0].id
            else None
        )

        assert asset_id is not None

        assert create_response is not None
        assets = create_response.assets or []
        assert len(assets) == 1
        asset_id = assets[0].id
        assert asset_id is not None

    def test__link_files__link_succeded(
        self, client: AssetManagementClient, create_asset
    ):
        self._create_assets_request[0].model_number = 101
        create_response = create_asset(self._create_assets_request)

        asset_id = (
            create_response.assets[0].id
            if create_response.assets and create_response.assets[0].id
            else None
        )

        assert asset_id is not None

        file_ids = ["608a5684800e325b48837c2a"]
        link_files_response = client.link_files(asset_id=asset_id, file_ids=file_ids)

        assert link_files_response is None
    
    def test__link_files__returns_error_when_asset_id_is_invalid(
        self, client: AssetManagementClient, create_asset
    ):
        invalid_asset_id = "invalid-asset-id"
        file_ids = ["608a5684800e325b48837c2a"]

        with pytest.raises(ApiException, match="NonExistingAssetWithIdentifier"):
            client.link_files(asset_id=invalid_asset_id, file_ids=file_ids)

    def test__delete_asset__returns_deleted_asset(self, client: AssetManagementClient):
        self._create_assets_request[0].model_number = 102
        create_response: CreateAssetsPartialSuccessResponse = client.create_assets(
            assets=self._create_assets_request
        )
        asset_id = (
            create_response.assets[0].id
            if create_response.assets and create_response.assets[0].id
            else None
        )

        assert asset_id is not None

        delete_response = client.delete_assets(ids=[asset_id])

        assert delete_response is not None
        assert delete_response.ids is not None
        assert len(delete_response.ids) == 1
        assert delete_response.ids[0] == asset_id

    def test__query_assets_with_take_value__returns_specific_number_of_assets(
        self, client: AssetManagementClient, create_asset
    ):
        self._create_assets_request[0].model_number = 103
        create_assets_response = create_asset(self._create_assets_request)

        assert create_assets_response is not None
        assert len(create_assets_response.assets) == 1

        asset_id = (
            create_assets_response.assets[0].id
            if create_assets_response.assets and create_assets_response.assets[0].id
            else None
        )

        query_assets_request = QueryAssetsRequest(
            skip=0, take=1, return_count=True, filter=f'id = "{asset_id}"'
        )

        response: QueryAssetsResponse = client.query_assets(query=query_assets_request)

        assert response is not None
        assert response.assets is not None and len(response.assets) == 1
        assert response.total_count is not None and response.total_count == 1

    def test_query_assets_with_projections__returns_the_assets_with_projected_properties(
        self, client: AssetManagementClient, create_asset
    ):
        self._create_assets_request[0].model_number = 103
        create_assets_response = create_asset(self._create_assets_request)

        assert create_assets_response is not None
        assert len(create_assets_response.assets) == 1

        asset_id = (
            create_assets_response.assets[0].id
            if create_assets_response.assets and create_assets_response.assets[0].id
            else None
        )
        query_asset = QueryAssetsRequest(
            filter=f'id = "{asset_id}"',
            projection=[AssetField.ID, AssetField.NAME],
            take=1,
        )
        response = client.query_assets(query=query_asset)

        assert response is not None
        assert response.assets is not None
        assert all(
            asset.id is not None
            and asset.name is not None
            and asset.bus_type is None
            and asset.calibration_status is None
            and asset.custom_calibration_interval is None
            and asset.discovery_type is None
            and asset.external_calibration is None
            and asset.file_ids is None
            and asset.firmware_version is None
            and asset.hardware_version is None
            and asset.is_NI_asset is None
            and asset.is_system_controller is None
            and asset.keywords is None
            and asset.last_updated_timestamp is None
            and asset.location is None
            and asset.model_name is None
            and asset.model_number is None
            and asset.asset_type is None
            and asset.out_for_calibration is None
            and asset.part_number is None
            and asset.properties is None
            and asset.self_calibration is None
            and asset.serial_number is None
            and asset.supports_external_calibration is None
            and asset.supports_reset is None
            and asset.supports_self_calibration is None
            and asset.supports_self_test is None
            and asset.temperature_sensors is None
            and asset.vendor_name is None
            and asset.vendor_number is None
            and asset.visa_resource_name is None
            and asset.workspace is None
            for asset in response.assets
        )
