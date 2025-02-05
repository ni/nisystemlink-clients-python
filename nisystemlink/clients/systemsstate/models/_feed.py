from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class Feed(JsonModel):
    """Model for object defining a feed, which contains the name, url, and Booleans
    for whether the feed is enabled and compressed
    """

    name: Optional[str] = None
    """Gets or sets name of the feed."""

    url: Optional[str] = None
    """Gets or sets the url for the repository."""

    enabled: bool
    """Gets or sets whether the feed is enabled or not."""

    compressed: bool
    """Gets or sets whether the feed is compressed or not."""
