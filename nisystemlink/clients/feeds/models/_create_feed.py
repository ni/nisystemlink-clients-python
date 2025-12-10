from __future__ import annotations

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._platform import Platform


class CreateFeedRequest(JsonModel):
    """Create Feed Request."""

    name: str
    """The name of the feed."""
    description: str | None = None
    """The description of the feed."""
    platform: Platform
    """The platform of the feed, the following package extensions are available: .nipkg for
    windows feeds, .ipk and .deb for ni-linux-rt feeds."""
    workspace: str | None = None
    """The ID of the workspace this feed belongs to. If the workspace is not defined,
    the default workspace is used."""
