"""Functionality of getting authentication information."""

from nisystemlink.clients.auth import AuthClient
from nisystemlink.clients.core import ApiException, HttpConfiguration


server_url = None # SystemLink API URL
server_api_key = None # SystemLink API key
workspace_name = None # Systemlink workspace name


auth_client = AuthClient(HttpConfiguration(server_uri=server_url, api_key=server_api_key))

try:
    caller_info = auth_client.authenticate()
    workspaces_info = caller_info.workspaces

    for workspace_info in workspaces_info:
        if workspace_info.name == workspace_name:
            print(workspace_info.id)

except ApiException as exp:
    print(exp)

except Exception as exp:
    print(exp)
