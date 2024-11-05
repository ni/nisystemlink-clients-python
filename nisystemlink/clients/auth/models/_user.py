from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class Status(Enum):
    """Enumeration to represent different status of user's registration."""

    PENDING = "pending"
    ACTIVE = "active"


class Org(JsonModel):
    """User's Organization information."""

    id: Optional[str] = None
    """The unique id."""
    name: Optional[str] = None
    """The name of the organization."""
    owner_id: Optional[str] = None
    """The userId of the organization owner."""


class User(JsonModel):
    """User information."""

    id: Optional[str] = None
    """The unique id."""
    first_name: Optional[str] = None
    """The user's first name."""
    last_name: Optional[str] = None
    """The user's last name."""
    email: Optional[str] = None
    """The user's email."""
    phone: Optional[str] = None
    """The user's contact phone number."""
    niua_id: Optional[str] = None
    """The external id (niuaId, SID, login name)."""
    login: Optional[str] = None
    """
    The login name of the user. This the "username" or equivalent entered when
    the user authenticates with the identity provider.
    """
    accepted_to_s: Optional[bool] = None
    """(deprecated) Whether the user accepted the terms of service."""
    properties: Optional[Dict[str, str]] = None
    """A map of key value properties."""
    keywords: Optional[List[str]] = None
    """A list of keywords associated with the user."""
    created: Optional[datetime] = None
    """The created timestamp."""
    updated: Optional[datetime] = None
    """The last updated timestamp."""
    org_id: Optional[str] = None
    """The id of the organization."""
    policies: Optional[List[str]] = None
    """A list of policy ids to reference existing policies."""
    status: Optional[Status] = None
    """The status of the users' registration."""
    entitlements: Optional[Any] = None
    """(deprecated) Features to which the user is entitled within the application."""
