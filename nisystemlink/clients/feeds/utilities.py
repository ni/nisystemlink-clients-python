"""Utilities for FeedsClient."""

from typing import List, Optional

from nisystemlink.clients.feeds.models import Feed


def get_feed_by_name(
    feeds: List[Feed],
    name: str,
) -> Optional[Feed]:
    """Get feed id from the list of feeds using `feed_name`.

    Args:
        feeds (List[Feed]): List of feeds.
        feed_name (str): Feed name.

    Returns:
        Optional[Feed]: Feed information.
    """
    for feed in feeds:
        if feed.name == name and feed.id:
            return feed
    return None
