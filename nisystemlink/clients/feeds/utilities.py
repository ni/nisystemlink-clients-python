"""Utilities for FeedsClient."""

from typing import List, Union

from nisystemlink.clients.feeds.models import Feed


def get_feed_id(
    feeds_details: List[Feed],
    feed_name: str,
) -> Union[str, None]:
    """Get feed id from the list of feed details using `feed_name`.

    Args:
        feeds_details (List[Feed]): List of feed details.
        feed_name (str): Feed name.

    Returns:
        Union[str, None]: Feed ID of the `feed_name`.
    """
    for feed in feeds_details:
        if feed.name == feed_name and feed.id:
            return feed.id
    return None
