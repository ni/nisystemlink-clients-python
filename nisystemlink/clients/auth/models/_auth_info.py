from __future__ import annotations

from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._auth_models import AuthPolicy, Error, Org, User, Workspace


class AuthInfo(JsonModel):
    """Information about the authenticated caller."""

    user: Optional[User]
    """Details of authenticated caller"""
    org: Optional[Org]
    """Organization of authenticated caller"""
    workspaces: Optional[List[Workspace]]
    """List of workspaces the authenticated caller has access"""
    policies: Optional[List[AuthPolicy]]
    """List of policies for the authenticated caller"""
    properties: Optional[Dict[str, str]] = Field(None, example={"key1": "value1"})
    """A map of key value properties"""
    error: Optional[Error]
    """Error response"""
