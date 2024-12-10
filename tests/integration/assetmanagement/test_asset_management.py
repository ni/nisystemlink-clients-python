from typing import List

import pytest
from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    Asset,
    AssetsCreatePartialSuccessResponse,
    AssetsResponse,
    AssetSummaryResponse,
    ConnectionHistoryResponse,
    DeleteAssetsResponse,
    ExportAssetsRequest,
    ExportAssetsResponse,
    QueryAssetRequest,
    QueryLocationHistoryRequest,
    UpdateAssetsPartialSuccessResponse,
)
from nisystemlink.clients.assetmanagement.models._asset import (
    AssetBusType,
    AssetDiscoveryType,
    AssetLocation,
    AssetPresence,
    AssetPresenceWithSystemConnection,
    AssetType,
    ExternalCalibration,
    SelfCalibration,
    TemperatureSensor,
)
from nisystemlink.clients.assetmanagement.models._asset_create import AssetCreate
from nisystemlink.clients.assetmanagement.models._asset_update import AssetUpdate
from nisystemlink.clients.assetmanagement.models._export_assets import (
    Destination,
    ResponseFormat,
)
from nisystemlink.clients.assetmanagement.models._query_location import (
    Destination as LocationDestination,
    ResponseFormat as LocationResponseFormat,
)
from nisystemlink.clients.core._api_exception import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture(scope="class")
def asset_create() -> List[AssetCreate]:
    """Fixture to create asset create object."""
    assets = [
        AssetCreate(
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
            partNumber="A1234 B5",
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

    def test__get_assets__returns_all_assets(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2001
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )

        response: AssetsResponse = client.get_assets()

        if create_assets_response.assets and create_assets_response.assets[0].id:
            client.delete_assets(ids=[create_assets_response.assets[0].id])

        assert response is not None
        assert response.total_count >= 1

    def test__get_assets_with_specific_take_value__returns_specific_number_of_assets(
        self, client: AssetManagementClient
    ):
        assets = []
        for i in range(10):
            assets.append(
                AssetCreate(
                    model_name="NI PXIe-6368",
                    model_number=2100 + i,
                    serial_number="01BB877A",
                    vendor_name="NI",
                    vendor_number="4244",
                    bus_type=AssetBusType.ACCESSORY,
                    name="PCISlot2",
                    asset_type=AssetType.DEVICE_UNDER_TEST,
                    firmware_version="A1",
                    hardware_version="12A",
                    visa_resource_name="vs-3144",
                    temperature_sensors=[
                        TemperatureSensor(name="Sensor0", reading=25.8)
                    ],
                    supports_self_calibration=True,
                    supports_external_calibration=True,
                    custom_calibration_interval=24,
                    self_calibration=SelfCalibration(
                        temperature_sensors=[
                            TemperatureSensor(name="Sensor0", reading=25.8)
                        ],
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
                        temperature_sensors=[
                            TemperatureSensor(name="Sensor0", reading=25.8)
                        ],
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
                    partNumber="A1234 B5",
                )
            )

        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=assets)
        )

        response: AssetsResponse = client.get_assets(take=10)

        ids = []
        if create_assets_response.assets:
            for asset in create_assets_response.assets:
                if asset.id:
                    ids.append(asset.id)

            client.delete_assets(ids=ids)

        assert response is not None
        assert response.total_count >= 10
        if response.assets:
            assert len(response.assets) == 10

    def test__get_assets_summary__returs_assets_summary(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2002
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )

        response: AssetSummaryResponse = client.get_asset_summary()

        if create_assets_response.assets and create_assets_response.assets[0].id:
            client.delete_assets(ids=[create_assets_response.assets[0].id])

        assert response is not None
        assert response.total >= 1
        assert response.total == response.active + response.not_active

    def test__get_asset_by_correct_id__returns_the_asset(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2003
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )

        if create_assets_response.assets and create_assets_response.assets[0].id:
            asset_id = create_assets_response.assets[0].id

        response: Asset = client.get_asset_by_id(asset_id=asset_id)

        if create_assets_response.assets and create_assets_response.assets[0].id:
            client.delete_assets(ids=[asset_id])

        assert response is not None
        assert response.model_number == 2003

    def test__get_asset_by_incorrect_id__does_not_return_the_asset(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"

        with pytest.raises(ApiException):
            client.get_asset_by_id(asset_id=asset_id)

    def test__create_one_asset__one_asset_gets_created(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2004

        response: AssetsCreatePartialSuccessResponse = client.create_assets(
            assets=asset_create
        )

        if response.assets and response.assets[0].id:
            client.delete_assets(ids=[response.assets[0].id])

        if response.assets:
            assert len(response.assets) == 1
            assert response.assets[0].model_number == 2004
        if response.failed:
            assert len(response.failed) == 0

    def test__create_multiple_assets__all_succeed(self, client: AssetManagementClient):
        assets = []
        for i in range(3):
            assets.append(
                AssetCreate(
                    model_name="NI PXIe-6368",
                    model_number=2200 + i,
                    serial_number="01BB877A",
                    vendor_name="NI",
                    vendor_number="4244",
                    bus_type=AssetBusType.ACCESSORY,
                    name="PCISlot2",
                    asset_type=AssetType.DEVICE_UNDER_TEST,
                    firmware_version="A1",
                    hardware_version="12A",
                    visa_resource_name="vs-3144",
                    temperature_sensors=[
                        TemperatureSensor(name="Sensor0", reading=25.8)
                    ],
                    supports_self_calibration=True,
                    supports_external_calibration=True,
                    custom_calibration_interval=24,
                    self_calibration=SelfCalibration(
                        temperature_sensors=[
                            TemperatureSensor(name="Sensor0", reading=25.8)
                        ],
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
                        temperature_sensors=[
                            TemperatureSensor(name="Sensor0", reading=25.8)
                        ],
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
                    partNumber="A1234 B5",
                )
            )

        response: AssetsCreatePartialSuccessResponse = client.create_assets(
            assets=assets
        )

        ids = []
        if response.assets and response.assets[0].id:
            for asset in response.assets:
                if asset.id:
                    ids.append(asset.id)

            client.delete_assets(ids=ids)

        if response.assets:
            assert len(response.assets) == 3
            assert response.assets[0].model_number == 2200
            assert response.assets[1].model_number == 2201
            assert response.assets[2].model_number == 2202
        if response.failed:
            assert len(response.failed) == 0

    def test__query_assets_with_take_value__returns_specific_number_of_assets(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2005
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )
        if create_assets_response.assets and create_assets_response.assets[0].id:
            asset_id = create_assets_response.assets[0].id
        query_assets_request = QueryAssetRequest(
            ids=[asset_id], skip=0, take=1, descending=False, calibratable_only=False
        )

        response: AssetsResponse = client.query_assets(query=query_assets_request)

        client.delete_assets(ids=[asset_id])

        assert response is not None
        if response.assets:
            assert len(response.assets) == 1
        assert response.total_count >= 1

    def test__export_assets__returns_file_ids(self, client: AssetManagementClient):
        request = ExportAssetsRequest(
            filter="",
            response_format=ResponseFormat.CSV,
            destination=Destination.FILE_SERVICE,
            file_ingestion_workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
        )

        response: ExportAssetsResponse = client.export_assets(export=request)

        assert response is not None
        if response.file_id:
            assert len(response.file_id) > 0

    def test__update_assets_with_correct_id__updates_assets(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2006
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )
        if create_assets_response.assets and create_assets_response.assets[0].id:
            asset_id = create_assets_response.assets[0].id

        assets = [
            AssetUpdate(
                model_name="Updated Model Name",
                model_number=3006,
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
                    temperature_sensors=[
                        TemperatureSensor(name="Sensor0", reading=25.8)
                    ],
                    is_limited=False,
                    date="2022-06-07T18:58:05.000Z",
                ),
                is_n_i_asset=True,
                id=asset_id,
                workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
                location=AssetLocation(
                    state=AssetPresenceWithSystemConnection(
                        asset_presence=AssetPresence.PRESENT
                    )
                ),
                external_calibration=ExternalCalibration(
                    temperature_sensors=[
                        TemperatureSensor(name="Sensor0", reading=25.8)
                    ],
                    date="2022-06-07T18:58:05.000Z",
                    recommended_interval=10,
                    next_recommended_date="2023-11-14T20:42:11.583Z",
                    next_custom_due_date="2024-11-14T20:42:11.583Z",
                    resolved_due_date="2022-06-07T18:58:05.000Z",
                ),
                properties={"Key1": "Value1"},
                keywords=["Keyword1"],
                file_ids=["608a5684800e325b48837c2a"],
                supports_self_test=True,
                supports_reset=True,
                partNumber="A1234 B5",
            )
        ]

        response: UpdateAssetsPartialSuccessResponse = client.update_assets(
            assets=assets
        )

        client.delete_assets(ids=[asset_id])

        assert response is not None
        if response.assets and response.assets[0].id and response.assets[0].model_name:
            assert response.assets[0].id == asset_id
            assert response.assets[0].model_name == "Updated Model Name"
        if response.failed:
            assert len(response.failed) == 0

    def test__update_assets_with_incorrect_id__does_not_update_assets(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"
        assets = [
            AssetUpdate(
                model_name="NI PXIe-6368",
                model_number=3006,
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
                    temperature_sensors=[
                        TemperatureSensor(name="Sensor0", reading=25.8)
                    ],
                    is_limited=False,
                    date="2022-06-07T18:58:05.000Z",
                ),
                is_n_i_asset=True,
                id=asset_id,
                workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
                location=AssetLocation(
                    state=AssetPresenceWithSystemConnection(
                        asset_presence=AssetPresence.PRESENT
                    )
                ),
                external_calibration=ExternalCalibration(
                    temperature_sensors=[
                        TemperatureSensor(name="Sensor0", reading=25.8)
                    ],
                    date="2022-06-07T18:58:05.000Z",
                    recommended_interval=10,
                    next_recommended_date="2023-11-14T20:42:11.583Z",
                    next_custom_due_date="2024-11-14T20:42:11.583Z",
                    resolved_due_date="2022-06-07T18:58:05.000Z",
                ),
                properties={"Key1": "Value1"},
                keywords=["Keyword1"],
                file_ids=["608a5684800e325b48837c2a"],
                supports_self_test=True,
                supports_reset=True,
                partNumber="A1234 B5",
            )
        ]

        response: UpdateAssetsPartialSuccessResponse = client.update_assets(
            assets=assets
        )

        assert response is not None
        if response.assets:
            assert len(response.assets) == 0
        if response.failed:
            assert len(response.failed) == 1

    def test__query_location_with_correct_id__returns_location_history(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2007
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )
        if create_assets_response.assets and create_assets_response.assets[0].id:
            asset_id = create_assets_response.assets[0].id
        query_location_request = QueryLocationHistoryRequest(
            take=0,
            continuation_token=None,
            response_format=LocationResponseFormat.JSON,
            destination=LocationDestination.INLINE,
            file_ingestion_workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
            location_filter="",
            start_time="2024-12-04T11:44:09.040Z",
            end_time="2024-12-04T11:44:09.040Z",
        )

        response: ConnectionHistoryResponse = client.query_location(
            asset_id=asset_id, query=query_location_request
        )

        client.delete_assets(ids=[asset_id])

        assert response is not None

    def test__query_location_with_incorrect_id__does_not_return_location_history(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"
        query_location_request = QueryLocationHistoryRequest(
            response_format=LocationResponseFormat.JSON,
            destination=LocationDestination.FILE_SERVICE,
        )

        with pytest.raises(ApiException):
            client.query_location(asset_id=asset_id, query=query_location_request)

    def test__delete_assets_with_Correct_id__deletes_assets(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2008
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )
        print(create_assets_response.error)
        if create_assets_response.assets and create_assets_response.assets[0].id:
            asset_id = create_assets_response.assets[0].id

        response: DeleteAssetsResponse = client.delete_assets(ids=[asset_id])

        assert response is not None
        if response.ids:
            assert response.ids[0] == asset_id

    def test__delete_assets_with_incorrect_id__fails(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect"

        response: DeleteAssetsResponse = client.delete_assets(ids=[asset_id])

        assert response is not None
        if response.ids:
            assert len(response.ids) == 0
        if response.failed:
            assert len(response.failed) == 1

    def test__link_files_with_correct_asset_id__links_files(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2009
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )
        request = ExportAssetsRequest(
            filter="",
            response_format=ResponseFormat.CSV,
            destination=Destination.FILE_SERVICE,
            file_ingestion_workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
        )
        export_assets_response: ExportAssetsResponse = client.export_assets(
            export=request
        )
        if create_assets_response.assets and create_assets_response.assets[0].id:
            asset_id = create_assets_response.assets[0].id
        if export_assets_response.file_id:
            file_ids = [export_assets_response.file_id]
            client.link_files(asset_id=asset_id, fileIds=file_ids)

        client.delete_assets(ids=[asset_id])

    def test__link_files_with_incorrect_asset_id__does_not_link_files(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"
        file_ids = ["608a5684800e325b48837c2a"]

        with pytest.raises(ApiException):
            client.link_files(asset_id=asset_id, fileIds=file_ids)

    def test__unlink_files_with_correct_asset_id__unlinks_files(
        self, client: AssetManagementClient, asset_create: List[AssetCreate]
    ):
        asset_create[0].model_number = 2010
        create_assets_response: AssetsCreatePartialSuccessResponse = (
            client.create_assets(assets=asset_create)
        )
        request = ExportAssetsRequest(
            filter="",
            response_format=ResponseFormat.CSV,
            destination=Destination.FILE_SERVICE,
            file_ingestion_workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
        )
        export_assets_response: ExportAssetsResponse = client.export_assets(
            export=request
        )
        if create_assets_response.assets and create_assets_response.assets[0].id:
            asset_id = create_assets_response.assets[0].id
        if export_assets_response.file_id:
            file_ids = [export_assets_response.file_id]
            client.link_files(asset_id=asset_id, fileIds=file_ids)

        client.unlink_files(asset_id=asset_id, file_id=file_ids[0])

        client.delete_assets(ids=[asset_id])

    def test__unlink_files_with_incorrect_asset_id__does_not_unlink_files(
        self, client: AssetManagementClient
    ):
        asset_id = "Incorrect Id"

        with pytest.raises(ApiException):
            client.unlink_files(asset_id=asset_id, file_id="608a5684800e325b48837c2a")
