from datetime import datetime, timezone

from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    AssetBusType,
    AssetDiscoveryType,
    AssetIdentificationModel,
    AssetLocationForCreate,
    AssetPresence,
    AssetPresenceStatus,
    AssetType,
    CreateAssetRequest,
    ExternalCalibration,
    QueryAssetsRequest,
    QueryAssetUtilizationHistoryRequest,
    SelfCalibration,
    StartUtilizationRequest,
    TemperatureSensor,
    UpdateUtilizationRequest,
    UtilizationOrderBy,
)
from nisystemlink.clients.core._http_configuration import HttpConfiguration

# workspace where the asset will be created
workspace_id = "yourWorkspaceId"
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = AssetManagementClient(configuration=server_configuration)

create_assets_request = [
    CreateAssetRequest(
        model_number=4000,
        model_name="NI PXIe-6368",
        serial_number="01BB877A",
        vendor_name="NI",
        vendor_number=4244,
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
            date=datetime(2022, 6, 7, 18, 58, 5, tzinfo=timezone.utc),
        ),
        is_NI_asset=True,
        workspace=workspace_id,
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
        discovery_type=AssetDiscoveryType.MANUAL,
        file_ids=["608a5684800e325b48837c2a"],
        supports_self_test=True,
        supports_reset=True,
        part_number="A1234 B5",
    )
]

# Create an asset.
create_assets_response = client.create_assets(assets=create_assets_request)

created_asset_id = None
if create_assets_response.assets and len(create_assets_response.assets) > 0:
    created_asset_id = str(create_assets_response.assets[0].id)

# Query assets using id.
query_asset_request = QueryAssetsRequest(
    filter=f'AssetIdentifier = "{created_asset_id}"',
    skip=0,
    take=1,
    descending=False,
    return_count=False,
)
client.query_assets(query=query_asset_request)

# Link files to the created asset.
file_ids = ["sample-file-id"]
if created_asset_id:
    link_files_response = client.link_files(
        asset_id=created_asset_id, file_ids=file_ids
    )

# Delete the created asset.
if created_asset_id is not None:
    client.delete_assets(ids=[created_asset_id])

# --- Asset Utilization Tracking Examples ---

# Start asset utilization tracking
start_utilization_request = StartUtilizationRequest(
    utilization_identifier="test-utilization-001",
    minion_id="test-minion-123",
    asset_identifications=[
        AssetIdentificationModel(
            model_name="NI PXIe-6368",
            model_number=4000,
            serial_number="01BB877A",
            vendor_name="NI",
            vendor_number=4244,
            bus_type=AssetBusType.ACCESSORY,
        )
    ],
    utilization_category="Testing",
    task_name="DUTTestingRoutine",
    user_name="testUser",
    utilization_timestamp=datetime.now(timezone.utc),
)

start_response = client.start_utilization(request=start_utilization_request)

# Send heartbeat to keep utilization session alive
if start_response.assets_with_started_utilization:
    heartbeat_request = UpdateUtilizationRequest(
        utilization_identifiers=["test-utilization-001"],
        utilization_timestamp=datetime.now(timezone.utc),
    )
    heartbeat_response = client.utilization_heartbeat(request=heartbeat_request)

# End asset utilization tracking
end_request = UpdateUtilizationRequest(
    utilization_identifiers=["test-utilization-001"],
    utilization_timestamp=datetime.now(timezone.utc),
)
end_response = client.end_utilization(request=end_request)

# Query asset utilization history
query_utilization_request = QueryAssetUtilizationHistoryRequest(
    utilization_filter='Category = "Testing"',
    asset_filter='ModelName = "NI PXIe-6368"',
    order_by=UtilizationOrderBy.START_TIMESTAMP,
    order_by_descending=True,
    take=10,
)

utilization_history = client.query_asset_utilization_history(
    request=query_utilization_request
)
