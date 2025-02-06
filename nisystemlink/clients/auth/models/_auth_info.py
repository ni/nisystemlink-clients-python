from __future__ import annotations

from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._auth_policy import AuthPolicy
from ._user import Org, User
from ._workspace import Workspace


class AuthInfo(JsonModel):
    """Information about the authenticated caller."""

    user: Optional[User] = None
    """Details of authenticated caller."""
    org: Optional[Org] = None
    """Organization of authenticated caller."""
    workspaces: Optional[List[Workspace]] = None
    """List of workspaces the authenticated caller has access."""
    policies: Optional[List[AuthPolicy]] = None
    """List of policies for the authenticated caller."""
    properties: Optional[Dict[str, str]] = None
    """A map of key value properties."""
