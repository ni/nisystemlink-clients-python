"""Functionality of deleting feed API."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient
from nisystemlink.clients.feeds.models import Platform
from nisystemlink.clients.feeds.utilities._get_feed_details import get_feed_by_name

# Update the constants.
FEED_NAME = ""
PLATFORM = Platform.WINDOWS
WORKSPACE_ID = (
    None  # None uses Default workspace. Replace with Systemlink workspace id.
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = FeedsClient(configuration=server_configuration)

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
