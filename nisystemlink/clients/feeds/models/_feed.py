from __future__ import annotations

from datetime import datetime
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._platform import Platform


class Feed(JsonModel):
    """Feed model."""

    id: str | None = None
    """The auto-generated ID of the feed."""
    name: str | None = None
    """The name of the feed."""
    description: str | None = None
    """The description of the feed."""
    platform: Platform | None = None
    """The platform of the feed, the following package extensions are available: .nipkg for
    windows feeds, .ipk and .deb for ni-linux-rt feeds.
    """
    workspace: str | None = None
    """The ID of the workspace this feed belongs to."""
    updated_at: datetime | None = None
    """The date of the latest feed update"""
    created_at: datetime | None = None
    """The date when the feed was created at."""
    package_sources: List[str] | None = None
    """The package sources list of the feed."""
    deleted: bool | None = None
    """Whether the feed deletion was requested."""
