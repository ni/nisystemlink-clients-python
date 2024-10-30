"""Example of getting workspace ID."""

from nisystemlink.clients.auth import AuthClient
from nisystemlink.clients.auth.utilities import get_workspace_id
from nisystemlink.clients.core import ApiException, HttpConfiguration


server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key
workspace_name = ""  # Systemlink workspace name

auth_client = AuthClient(
    HttpConfiguration(server_uri=server_url, api_key=server_api_key)
)

try:
    caller_info = auth_client.authenticate()
    workspaces_info = caller_info.workspaces
    workspace_id = None

    if workspaces_info:
        workspace_id = get_workspace_id(
            workspaces_info=workspaces_info,
            workspace_name=workspace_name,
        )

    if workspace_id:
        print(f"Workspace ID: {workspace_id}")

except ApiException as exp:
    print(exp)

except Exception as exp:
    print(exp)
