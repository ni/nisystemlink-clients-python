from datetime import datetime, timezone
from typing import Callable, Generator, List
from uuid import uuid4

import pytest
from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    Asset,
    AssetBusType,
    AssetDiscoveryType,
    AssetField,
    AssetIdentification,
    AssetLocationForCreate,
    AssetPresence,
    AssetPresenceStatus,
    AssetType,
    CreateAssetRequest,
    CreateAssetsPartialSuccessResponse,
    ExternalCalibration,
    QueryAssetsRequest,
    QueryAssetsResponse,
    QueryAssetUtilizationHistoryRequest,
    SelfCalibration,
    StartUtilizationRequest,
    TemperatureSensor,
    UtilizationOrderBy,
)
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture
def create_asset(
    client: AssetManagementClient,
) -> Generator[
    Callable[[List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse], None, None
]:
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


@pytest.fixture
def unique_identifier() -> str:
    """Fixture to generate a unique identifier using UUID"""
    return str(uuid4())


@pytest.fixture
def start_utilization(
    client: AssetManagementClient,
) -> Generator[Callable[[str, List[Asset], str, str, str, str], None], None, None]:
    """Fixture to start utilization and automatically clean up."""
    started_utilizations: List[str] = []

    def _start_utilization(
        utilization_id: str,
        assets: List[Asset],
        minion_id: str,
        task_name: str,
        category: str,
        user_name: str,
    ) -> None:
        asset_identifications = [
            AssetIdentification(
                model_name=asset.model_name,
                model_number=asset.model_number,
                serial_number=asset.serial_number,
                vendor_name=asset.vendor_name,
                vendor_number=asset.vendor_number,
                bus_type=asset.bus_type,
            )
            for asset in assets
        ]
        start_request = StartUtilizationRequest(
            utilization_identifier=utilization_id,
            minion_id=minion_id,
            asset_identifications=asset_identifications,
            utilization_category=category,
            task_name=task_name,
            user_name=user_name,
            utilization_timestamp=datetime.now(),
        )
        client.start_utilization(request=start_request)
        started_utilizations.append(utilization_id)

    yield _start_utilization

    # Cleanup: end all started utilizations
    if started_utilizations:
        client.end_utilization(
            ids=started_utilizations,
            timestamp=datetime.now(),
        )


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
            vendor_number=4244,
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
                date=datetime(2022, 6, 7, 18, 58, 5, tzinfo=timezone.utc),
            ),
            is_NI_asset=True,
            workspace=_workspace,
            location=AssetLocationForCreate(
                state=AssetPresence(asset_presence=AssetPresenceStatus.PRESENT)
            ),
            external_calibration=ExternalCalibration(
                temperature_sensors=[TemperatureSensor(name="Sensor0", reading=25.8)],
                date=datetime(2022, 6, 7, 18, 58, 5, tzinfo=timezone.utc),
                recommended_interval=10,
                next_recommended_date=datetime(
                    2023, 11, 14, 20, 42, 11, 583000, tzinfo=timezone.utc
                ),
                next_custom_due_date=datetime(
                    2024, 11, 14, 20, 42, 11, 583000, tzinfo=timezone.utc
                ),
                resolved_due_date=datetime(2022, 6, 7, 18, 58, 5, tzinfo=timezone.utc),
            ),
            properties={"Key1": "Value1"},
            keywords=["Keyword1"],
            discovery_type=AssetDiscoveryType.AUTOMATIC,
            file_ids=["608a5684800e325b48837c2a"],
            supports_self_test=True,
            supports_reset=True,
            part_number="A1234",
        )
    ]
    """CreateAssetRequest object"""

    def test__create_asset__returns_created_asset(
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
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
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
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
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
    ):
        self._create_assets_request[0].model_number = 103
        create_assets_response = create_asset(self._create_assets_request)

        assert create_assets_response is not None
        assert create_assets_response.assets is not None
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
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
    ):
        self._create_assets_request[0].model_number = 103
        create_assets_response = create_asset(self._create_assets_request)

        assert create_assets_response is not None
        assert create_assets_response.assets is not None
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

    def test__start_utilization__returns_success_response(
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
        unique_identifier: str,
        start_utilization: Callable[[str, List[Asset], str, str, str, str], None],
    ):
        # Create an asset to use for utilization tracking
        self._create_assets_request[0].model_number = 105
        create_response = create_asset(self._create_assets_request)

        assert create_response.assets is not None and len(create_response.assets) == 1
        created_asset = create_response.assets[0]

        # Start utilization tracking
        start_utilization(
            unique_identifier,
            [created_asset],
            "test-minion-python",
            "PythonIntegrationTest",
            "Testing",
            "test_user",
        )

        # Verify utilization was started by querying
        query_request = QueryAssetUtilizationHistoryRequest(
            utilization_filter=f'UtilizationIdentifier = "{unique_identifier}"',
            asset_filter=f'AssetIdentifier = "{created_asset.id}"',
        )
        query_response = client.query_asset_utilization_history(request=query_request)

        assert query_response is not None
        assert query_response.asset_utilizations is not None
        assert len(query_response.asset_utilizations) >= 1
        assert (
            query_response.asset_utilizations[0].utilization_identifier
            == unique_identifier
        )

    def test__utilization_heartbeat__returns_success_response(
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
        unique_identifier: str,
        start_utilization: Callable[[str, List[Asset], str, str, str, str], None],
    ):
        # Create multiple assets for utilization tracking
        self._create_assets_request[0].model_number = 106
        self._create_assets_request[0].serial_number = "106A"
        create_response1 = create_asset(self._create_assets_request)

        self._create_assets_request[0].model_number = 106
        self._create_assets_request[0].serial_number = "106B"
        create_response2 = create_asset(self._create_assets_request)

        assert create_response1.assets is not None and len(create_response1.assets) == 1
        assert create_response2.assets is not None and len(create_response2.assets) == 1
        created_assets = [create_response1.assets[0], create_response2.assets[0]]

        utilization_id = unique_identifier
        start_utilization(
            utilization_id,
            created_assets,
            "test-minion-python",
            "PythonIntegrationTest",
            "Testing",
            "test_user",
        )

        # Send heartbeat
        heartbeat_response = client.utilization_heartbeat(
            ids=[utilization_id],
            timestamp=datetime.now(),
        )

        assert heartbeat_response is not None
        assert heartbeat_response.updated_utilization_ids is not None
        assert len(heartbeat_response.updated_utilization_ids) == 1
        assert heartbeat_response.updated_utilization_ids[0] == utilization_id

    def test__end_utilization__returns_success_response(
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
        unique_identifier: str,
        start_utilization: Callable[[str, List[Asset], str, str, str, str], None],
    ):
        # Create multiple assets for utilization tracking
        self._create_assets_request[0].model_number = 107
        self._create_assets_request[0].serial_number = "107A"
        create_response1 = create_asset(self._create_assets_request)

        self._create_assets_request[0].model_number = 107
        self._create_assets_request[0].serial_number = "107B"
        create_response2 = create_asset(self._create_assets_request)

        assert create_response1.assets is not None and len(create_response1.assets) == 1
        assert create_response2.assets is not None and len(create_response2.assets) == 1
        created_assets = [create_response1.assets[0], create_response2.assets[0]]

        utilization_id = unique_identifier
        start_utilization(
            utilization_id,
            created_assets,
            "test-minion-python",
            "PythonIntegrationTest",
            "Testing",
            "test_user",
        )

        # End utilization
        end_response = client.end_utilization(
            ids=[utilization_id],
            timestamp=datetime.now(),
        )

        assert end_response is not None
        assert end_response.updated_utilization_ids is not None
        assert len(end_response.updated_utilization_ids) == 1
        assert end_response.updated_utilization_ids[0] == utilization_id

    def test__query_asset_utilization_history__returns_response(
        self,
        client: AssetManagementClient,
        create_asset: Callable[
            [List[CreateAssetRequest]], CreateAssetsPartialSuccessResponse
        ],
        unique_identifier: str,
        start_utilization: Callable[[str, List[Asset], str, str, str, str], None],
    ):
        # Create an asset, start and end utilization to create history
        self._create_assets_request[0].model_number = 108
        create_response = create_asset(self._create_assets_request)

        assert create_response.assets is not None and len(create_response.assets) == 1
        created_asset = create_response.assets[0]

        utilization_id = unique_identifier
        minion_id = "test-minion-python"
        category = "Testing"
        task_name = "PythonQueryTest"
        user_name = "test_user"

        # Start utilization
        start_utilization(
            utilization_id, [created_asset], minion_id, task_name, category, user_name
        )

        # End utilization
        client.end_utilization(
            ids=[utilization_id],
            timestamp=datetime.now(),
        )

        # Query utilization history - filter by asset ID to limit scope
        query_request = QueryAssetUtilizationHistoryRequest(
            utilization_filter=f'UtilizationIdentifier = "{utilization_id}"',
            asset_filter=f'AssetIdentifier = "{created_asset.id}"',
            order_by=UtilizationOrderBy.START_TIMESTAMP,
            order_by_descending=True,
            take=10,
        )

        query_response = client.query_asset_utilization_history(request=query_request)

        assert query_response is not None
        assert query_response.asset_utilizations is not None
        assert len(query_response.asset_utilizations) >= 1

        # Verify continuation_token exists (from WithPaging)
        assert hasattr(query_response, "continuation_token")

        # Find our utilization record
        utilization = query_response.asset_utilizations[0]

        # Verify the utilization data matches what we created
        assert utilization.utilization_identifier == utilization_id
        assert utilization.minion_id == minion_id
        assert utilization.category == category
        assert utilization.task_name == task_name
        assert utilization.user_name == user_name
        assert utilization.asset_identifier == created_asset.id
        assert utilization.start_timestamp is not None
        assert isinstance(utilization.start_timestamp, datetime)
        assert utilization.end_timestamp is not None
        assert isinstance(utilization.end_timestamp, datetime)
        assert isinstance(utilization.heartbeat_timestamp, datetime)

    def test__start_utilization_with_nonexistent_asset__raises_ApiException(
        self, client: AssetManagementClient, unique_identifier: str
    ):
        start_request = StartUtilizationRequest(
            utilization_identifier=unique_identifier,
            minion_id="test-minion",
            asset_identifications=[
                AssetIdentification(
                    model_name="TestModel",
                    serial_number="TEST123",
                    vendor_name="TestVendor",
                    vendor_number=1234,
                    bus_type=AssetBusType.ACCESSORY,
                )
            ],
            utilization_timestamp=datetime.now(),
        )

        with pytest.raises(ApiException):
            client.start_utilization(request=start_request)

    def test__heartbeat_with_nonexistent_utilization_id__returns_empty_list(
        self, client: AssetManagementClient, unique_identifier: str
    ):
        response = client.utilization_heartbeat(
            ids=[unique_identifier],
            timestamp=datetime.now(),
        )

        assert response is not None
        assert response.updated_utilization_ids is not None
        assert len(response.updated_utilization_ids) == 0

    def test__end_utilization_with_nonexistent_utilization_id__returns_empty_list(
        self, client: AssetManagementClient, unique_identifier: str
    ):
        response = client.end_utilization(
            ids=[unique_identifier],
            timestamp=datetime.now(),
        )

        assert response is not None
        assert response.updated_utilization_ids is not None
        assert len(response.updated_utilization_ids) == 0

    def test__query_utilization_history_with_invalid_filter__raises_ApiException(
        self, client: AssetManagementClient
    ):
        query_request = QueryAssetUtilizationHistoryRequest(
            utilization_filter="InvalidField = 'test'",
        )

        with pytest.raises(ApiException):
            client.query_asset_utilization_history(request=query_request)
