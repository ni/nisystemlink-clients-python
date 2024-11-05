"""Functionality of deleting feed API."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient
from nisystemlink.clients.feeds.models import Platform
from nisystemlink.clients.feeds.utilities import get_feed_by_name

# Update the constants.
FEED_NAME = ""
PLATFORM = Platform.WINDOWS
WORKSPACE_ID = (
    None # None uses Default workspace. Replace with Systemlink workspace id.
)

server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key

# Provide the valid API key and API URL for client intialization.
client = FeedsClient(HttpConfiguration(api_key=server_api_key, server_uri=server_url))

# Deleting Feed.
try:
    # Get ID of the Feed to delete by name
    feeds = client.query_feeds(platform=PLATFORM, workspace=WORKSPACE_ID)
    feed = get_feed_by_name(feeds=feeds, name=FEED_NAME)
    feed_id = feed.id if feed else None

    # Delete the Feed by ID
    if feed_id:
        client.delete_feed(id=feed_id)
        print("Feed deleted successfully.")

except ApiException as exp:
    print(exp)
except Exception as exp:
    print(exp)
