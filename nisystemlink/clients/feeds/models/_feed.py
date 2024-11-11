from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._platform import Platform


class Feed(JsonModel):
    """Feed model."""

    id: Optional[str] = None
    """The auto-generated ID of the feed."""
    name: Optional[str] = None
    """The name of the feed."""
    description: Optional[str] = None
    """The description of the feed."""
    platform: Optional[Platform] = None
    """The platform of the feed, the following package extensions are available: .nipkg for
    windows feeds, .ipk and .deb for ni-linux-rt feeds.
    """
    workspace: Optional[str] = None
    """The ID of the workspace this feed belongs to."""
    updated_at: Optional[datetime] = None
    """The date of the latest feed update"""
    created_at: Optional[datetime] = None
    """The date when the feed was created at."""
    package_sources: Optional[List[str]] = None
    """The package sources list of the feed."""
    deleted: Optional[bool] = None
    """Whether the feed deletion was requested."""
