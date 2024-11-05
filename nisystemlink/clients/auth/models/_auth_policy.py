from __future__ import annotations

from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AuthStatement(JsonModel):
    """Auth Statement information."""

    actions: Optional[List[str]] = None
    """A list of actions the user is allowed to perform.

    example: notebookexecution:Query
    """
    resource: Optional[List[str]] = None
    """A list of resources the user is allowed to access.

    example: Notebook
    """
    workspace: Optional[str] = None
    """The workspace the user is allowed to access.

    example: 5afb2ce3741fe11d88838cc9
    """


class Statement(AuthStatement):
    """Statement information."""

    description: Optional[str] = None
    """A description for this statement."""


class AuthPolicy(JsonModel):
    """Auth Policy information."""

    statements: Optional[List[AuthStatement]] = None
    """A list of statements defining the actions the user can perform on a resource in a workspace.
    """
