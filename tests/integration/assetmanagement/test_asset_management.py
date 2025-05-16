from typing import List

import pytest
from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    AssetBusType,
    AssetCreateRequest,
    AssetDiscoveryType,
    AssetLocation,
    AssetPresence,
    AssetPresenceWithSystemConnection,
    AssetsCreatePartialSuccessResponse,
    AssetType,
    ExternalCalibration,
    QueryAssetsRequest,
    QueryAssetsResponse,
    SelfCalibration,
    TemperatureSensor,
)
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture(scope="class")
def create_assets_request() -> List[AssetCreateRequest]:
    """Fixture to create an AssetCreateRequest object."""
    assets = [
        AssetCreateRequest(
            model_name="NI PXIe-6368",
            serial_number="01BB877A",
            vendor_name="NI",
            vendor_number="4244",
            bus_type=AssetBusType.ACCESSORY,
            name="PCISlot2",
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
            is_n_i_asset=True,
            workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
            location=AssetLocation(
                state=AssetPresenceWithSystemConnection(
                    asset_presence=AssetPresence.PRESENT
                )
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
            part_number="A1234 B5",
        )
    ]

    return assets


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> AssetManagementClient:
    """Fixture to create a AssetManagementClient instance"""
    return AssetManagementClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestAssetManagement:

    def test__create_asset__returns_created_asset(
        self,
        client: AssetManagementClient,
        create_assets_request: List[AssetCreateRequest],
    ):
        create_assets_request[0].model_number = 101
        create_response: AssetsCreatePartialSuccessResponse = client.create_assets(
            assets=create_assets_request
        )

        asset_id = (
            create_response.assets[0].id
            if create_response.assets and create_response.assets[0].id
            else None
        )

        assert asset_id is not None

        client.delete_assets(ids=[asset_id])

        assert create_response is not None
        assets = create_response.assets or []
        assert len(assets) == 1
        asset_id = assets[0].id
        assert asset_id is not None

    def test__delete_asset__returns_deleted_asset(
        self,
        client: AssetManagementClient,
        create_assets_request: List[AssetCreateRequest],
    ):
        create_assets_request[0].model_number = 102
        create_response: AssetsCreatePartialSuccessResponse = client.create_assets(
            assets=create_assets_request
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
        self,
        client: AssetManagementClient,
        create_assets_request: List[AssetCreateRequest],
    ):
        create_assets_request[0].model_number = 103
        create_response: AssetsCreatePartialSuccessResponse = client.create_assets(
            assets=create_assets_request
        )
        asset_id = (
            create_response.assets[0].id
            if create_response.assets and create_response.assets[0].id
            else None
        )

        assert asset_id is not None

        query_request = QueryAssetsRequest(
            ids=[asset_id],
            skip=0,
            take=1,
            descending=False,
            calibratable_only=False,
            returnCount=True,
        )
        response: QueryAssetsResponse = client.query_assets(query=query_request)

        client.delete_assets(ids=[asset_id])

        assert response is not None
        assert response.assets is not None and len(response.assets) == 1
        assert response.total_count >= 1
