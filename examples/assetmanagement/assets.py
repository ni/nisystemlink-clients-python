from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    AssetBusType,
    AssetDiscoveryType,
    AssetLocationForCreate,
    AssetPresence,
    AssetPresenceStatus,
    AssetType,
    CreateAssetRequest,
    ExternalCalibration,
    QueryAssetsRequest,
    SelfCalibration,
    TemperatureSensor,
)
from nisystemlink.clients.core._http_configuration import HttpConfiguration


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
        is_NI_asset=True,
        workspace="your-workspace-id",
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
        discovery_type=AssetDiscoveryType.MANUAL,
        file_ids=["608a5684800e325b48837c2a"],
        supports_self_test=True,
        supports_reset=True,
        partNumber="A1234 B5",
    )
]

# Create an asset.
create_assets_response = client.create_assets(assets=create_assets_request)

created_asset_id = None
if create_assets_response.assets and len(create_assets_response.assets) > 0:
    created_asset_id = str(create_assets_response.assets[0].id)

# Query assets using id.
query_asset_request = QueryAssetsRequest(
    ids=[created_asset_id],
    skip=0,
    take=1,
    descending=False,
    calibratable_only=False,
    returnCount=False,
)
client.query_assets(query=query_asset_request)

# Delete the created asset.
if created_asset_id is not None:
    client.delete_assets(ids=[created_asset_id])
