from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.systems._systems_client import SystemsClient
from nisystemlink.clients.systems.models._create_virtual_systems_request import (
    CreateVirtualSystemRequest,
)
from nisystemlink.clients.systems.models._query_systems_request import (
    QuerySystemsRequest,
)

# Setup the server configuration to point to your instance of
# SystemLink Enterprise.
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = SystemsClient(configuration=server_configuration)

# Systems request metadata.
create_virtual_system_request: CreateVirtualSystemRequest = CreateVirtualSystemRequest(
    alias="Python integration virtual system",
    workspace="your-workspace-id",
)

# Create a virtual system.
create_virtual_system_response = client.create_virtual_system(
    create_virtual_system_request=create_virtual_system_request
)

minion_id = None

if create_virtual_system_response and create_virtual_system_response.minionId:
    minion_id = create_virtual_system_response.minionId

# Query systems using id.
query_systems_request = QuerySystemsRequest(
    filter=f'id="{minion_id}"', projection="new(id, alias)"
)

client.query_systems(query=query_systems_request)

# Delete the created systems.
if minion_id is not None:
    remove_systems = [minion_id]
    client.remove_systems(tgt=remove_systems)
