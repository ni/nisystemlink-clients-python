import threading
import time
from datetime import datetime
from uuid import uuid4

from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import (
    AssetBusType,
    AssetIdentification,
    AssetLocationForCreate,
    AssetPresence,
    AssetPresenceStatus,
    CreateAssetRequest,
    StartUtilizationRequest,
)
from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.core.helpers import read_minion_id

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = AssetManagementClient(configuration=server_configuration)

# Generate a unique identifier for this utilization session
utilization_id = str(uuid4())

# Create the assets first
# Define the assets to be created and used in the test
create_assets_request = [
    CreateAssetRequest(
        model_name="NI PXIe-6368",
        model_number=4000,
        serial_number="01BB877A",
        vendor_name="NI",
        vendor_number=4244,
        bus_type=AssetBusType.ACCESSORY,
        name="DAQ Device - 01BB877A",
        location=AssetLocationForCreate(
            state=AssetPresence(asset_presence=AssetPresenceStatus.PRESENT)
        ),
    ),
    CreateAssetRequest(
        model_name="NI PXIe-5163",
        model_number=5000,
        serial_number="02CC988B",
        vendor_name="NI",
        vendor_number=4244,
        bus_type=AssetBusType.ACCESSORY,
        name="Oscilloscope - 02CC988B",
        location=AssetLocationForCreate(
            state=AssetPresence(asset_presence=AssetPresenceStatus.PRESENT)
        ),
    ),
]

# Create the assets in SystemLink
create_assets_response = client.create_assets(assets=create_assets_request)

if create_assets_response.assets:
    print(f"Created {len(create_assets_response.assets)} asset(s)")
    created_asset_ids = [
        asset.id for asset in create_assets_response.assets if asset.id
    ]
else:
    print("Failed to create assets")
    exit(1)

# Define the asset identifications for utilization tracking
test_assets = [
    AssetIdentification(
        model_name="NI PXIe-6368",
        model_number=4000,
        serial_number="01BB877A",
        vendor_name="NI",
        vendor_number=4244,
        bus_type=AssetBusType.ACCESSORY,
    ),
    AssetIdentification(
        model_name="NI PXIe-5163",
        model_number=5000,
        serial_number="02CC988B",
        vendor_name="NI",
        vendor_number=4244,
        bus_type=AssetBusType.ACCESSORY,
    ),
]

# Start asset utilization tracking
# This marks the assets as "in use" in the SystemLink UI
# Read the minion ID from the Salt configuration
minion_id = read_minion_id() or "test-station-01"  # Fallback minion ID if not found

start_utilization_request = StartUtilizationRequest(
    utilization_identifier=utilization_id,
    minion_id=minion_id,
    asset_identifications=test_assets,
    utilization_category="Automated Testing",
    task_name="DUT Validation Suite",
    user_name="automation_user",
    utilization_timestamp=datetime.now(),
)

start_utilization_response = client.start_utilization(request=start_utilization_request)

print(start_utilization_response)

# Verify utilization started successfully
if start_utilization_response.assets_with_started_utilization:
    print(
        f"Utilization started for {len(start_utilization_response.assets_with_started_utilization)} asset(s)"
    )
else:
    print("Failed to start utilization")


# Heartbeat mechanism using a background thread
# IMPORTANT: Heartbeats are for UI purposes only, to keep assets visually
# marked as "in use" in the SystemLink UI. This applies only to utilizations
# that have not been ended. While the standard heartbeat interval is 5 minutes,
# the UI requires heartbeats at least every 10 minutes to continue showing
# assets as actively utilized. If heartbeats stop, the assets will no longer
# appear as "in use" in the UI.
heartbeat_interval = 300  # 5 minutes in seconds
stop_event = threading.Event()


def heartbeat_loop():
    """Background thread that sends periodic heartbeats.

    This keeps the asset visually marked as "in use" in the SystemLink UI
    (for UI purposes only). Applies only to utilizations that have not been ended.
    The UI requires heartbeats at least every 10 minutes to continue displaying
    the asset as actively utilized.
    """
    while not stop_event.wait(heartbeat_interval):
        heartbeat_response = client.utilization_heartbeat(
            ids=[utilization_id],
            timestamp=datetime.now(),
        )

        if heartbeat_response.updated_utilization_ids:
            print(
                f"Heartbeat sent at {datetime.now().strftime('%H:%M:%S')} - asset remains 'in use'"
            )


# Start the heartbeat thread
heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
heartbeat_thread.start()

# Simulate a long-running operation where assets are in use
# In a real scenario, this would be your actual test or operation
print("\nAssets are now in use. Heartbeats will be sent every 5 minutes...")
print("Waiting for 10 minutes to demonstrate heartbeats...\n")

time.sleep(600)  # Wait 10 minutes

# Stop the heartbeat thread
stop_event.set()
heartbeat_thread.join()

# End asset utilization tracking
end_utilization_response = client.end_utilization(
    ids=[utilization_id],
    timestamp=datetime.now(),
)

if end_utilization_response.updated_utilization_ids:
    print("\nUtilization ended - asset(s) released")

# Clean up: delete the created assets
if created_asset_ids:
    client.delete_assets(ids=created_asset_ids)
    print(f"Deleted {len(created_asset_ids)} asset(s)")
