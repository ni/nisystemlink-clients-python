"""Get workspace information."""

from typing import List, Optional

from nisystemlink.clients.auth.models import Workspace


def get_workspace_by_name(
    workspaces: List[Workspace],
    name: str,
) -> Optional[Workspace]:
    """Get workspace information from the list of workspace using `name`.

    Args:
        workspaces (List[Workspace]): List of workspace.
        name (str): Workspace name.

    Returns:
        Optional[Workspace]: Workspace information.
    """
    for workspace in workspaces:
        if workspace.name == name and workspace.id:
            return workspace
    return None
