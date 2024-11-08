from __future__ import annotations

from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class Workspace(JsonModel):
    """Workspace information."""

    id: Optional[str] = None
    """The unique id."""
    name: Optional[str] = None
    """The workspace name."""
    enabled: Optional[bool] = None
    """Whether the workspace is enabled or not."""
    default: Optional[bool] = None
    """
    Whether the workspace is the default. The default workspace is used when callers omit a \
workspace id.
    """
