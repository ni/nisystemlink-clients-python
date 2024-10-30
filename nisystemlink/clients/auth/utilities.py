"""Utilities for Auth Client."""

from typing import List, Union

from nisystemlink.clients.auth.models import Workspace


def get_workspace_id(
    workspaces_info: List[Workspace],
    workspace_name: str,
) -> Union[str, None]:
    """Get workspace id from the list of workspace info using `workspace_name`.

    Args:
        workspaces_info (List[workspace_info]): List of workspace info.
        workspace_name (str): Workspace name.

    Returns:
        Union[str, None]: Workspace ID of the `workspace_name`.
    """
    for workspace_info in workspaces_info:
        if workspace_info.name == workspace_name and workspace_info.id:
            return workspace_info.id
    return None
