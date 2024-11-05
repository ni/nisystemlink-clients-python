"""Example of getting workspace ID."""

from nisystemlink.clients.auth import AuthClient
from nisystemlink.clients.auth.utilities import get_workspace_by_name
from nisystemlink.clients.core import ApiException, HttpConfiguration


server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key
workspace_name = ""  # Systemlink workspace name

auth_client = AuthClient(
    HttpConfiguration(server_uri=server_url, api_key=server_api_key)
)

try:
    caller_info = auth_client.get_auth_info()
    workspaces = caller_info.workspaces if caller_info.workspaces else None
    workspace_id = None

    if workspaces:
        workspace_info = get_workspace_by_name(
            workspaces=workspaces,
            name=workspace_name,
        )
        workspace_id = workspace_info.id if workspace_info else None

    if workspace_id:
        print(f"Workspace ID: {workspace_id}")

except ApiException as exp:
    print(exp)

except Exception as exp:
    print(exp)
