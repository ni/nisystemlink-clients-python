from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.systems import SystemsClient
from nisystemlink.clients.systems.models import (
    CreateVirtualSystemRequest,
    QuerySystemsRequest,
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

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
