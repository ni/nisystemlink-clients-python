# Setup the server configuration to point to your instance of SystemLink Enterprise
from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    ExportAssetsRequest,
    QueryAssetRequest,
    QueryLocationHistoryRequest,
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
from nisystemlink.clients.core._http_configuration import HttpConfiguration


def create_an_asset():
    """Create an example asset in your server."""
    assets = [
        AssetCreate(
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

    response = client.create_assets(assets=assets)
    return response


# Setup the server configuration to point to your instance of SystemLink Enterprise.
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = AssetManagementClient(configuration=server_configuration)


# Get first 10 assets using take attribute in get all method.
getAssetsResponse = client.get_assets(take=10)

createAssetResponse = create_an_asset()

# Get the created asset.
getAssetResponse = client.get_asset_by_id(asset_id=createAssetResponse.assets[0].id)

# Get asset summary.
summaryResponse = client.get_asset_summary()

# Query assets using id.
queryRequest = QueryAssetRequest(
    ids=[createAssetResponse.assets[0].id],
    skip=0,
    take=1,
    descending=False,
    calibratable_only=False,
)
queryResponse = client.query_assets(queryRequest)

# Export assets report.
exportRequest = ExportAssetsRequest(
    response_format=ResponseFormat.CSV,
    destination=Destination.FILE_SERVICE,
    file_ingestion_workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
)
exportResponse = client.export_assets(export=exportRequest)

# Update the created asset.
updateAssets = [
    AssetUpdate(
        model_name="Updated Model Name",
        model_number=4001,
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
        id=createAssetResponse.assets[0].id,
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
        file_ids=["608a5684800e325b48837c2a"],
        supports_self_test=True,
        supports_reset=True,
        partNumber="A1234 B5",
    )
]
updatedResponse = client.update_assets(assets=updateAssets)

# Query asset location history of the created asset.
queryLocationRequest = QueryLocationHistoryRequest(
    response_format=LocationResponseFormat.JSON,
    destination=LocationDestination.FILE_SERVICE,
)
queryLocationResponse = client.query_location(
    query=queryLocationRequest, asset_id=createAssetResponse.assets[0].id
)

# Link files to the created asset.
if exportResponse.file_id:
    fileIds = [exportResponse.file_id]
    linkFilesResponse = client.link_files(
        fileIds=fileIds, asset_id=createAssetResponse.assets[0].id
    )

# Unlink a file from the created asset.
client.unlink_files(asset_id=createAssetResponse.assets[0].id, file_id=fileIds[0])

# Delete the created asset.
client.delete_assets(ids=[createAssetResponse.assets[0].id])
