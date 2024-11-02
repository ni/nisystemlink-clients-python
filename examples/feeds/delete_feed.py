"""Functionality of deleting feed API."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient
from nisystemlink.clients.feeds.models import Platform
from nisystemlink.clients.feeds.utilities import get_feed_by_name


FEED_NAME = "EXAMPLE FEED"  # Name of the feed.
PLATFORM = Platform.WINDOWS

server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key
workspace_id = (
    None  # None uses Default workspace. Replace with Systemlink workspace id.
)

# Please provide the valid API key and API URL for client intialization.
client = FeedsClient(HttpConfiguration(api_key=server_api_key, server_uri=server_url))

# Deleting Feed.
try:
    # To query available feeds.
    query_feeds_response = client.query_feeds(platform=PLATFORM, workspace=workspace_id)
    feed_details = get_feed_by_name(feeds=query_feeds_response, name=FEED_NAME)

    if feed_details and feed_details.id:
        created_feed_name = client.delete_feed(id=feed_details.id)
        print("Feed deleted successfully.")

except ApiException as exp:
    print(exp)
except Exception as exp:
    print(exp)
