"""Functionality of creating feeds APIs."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient
from nisystemlink.clients.feeds.models import (
    CreateFeedRequest,
    Platform,
)


FEED_NAME = "EXAMPLE FEED"
FEED_DESCRIPTION = "EXAMPLE DESCRIPTION"
PLATFORM = Platform.WINDOWS.value

server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key
workspace_id = ""  # Systemlink workspace id

# Please provide the valid API key and API URL for client intialization.
client = FeedsClient(HttpConfiguration(api_key=server_api_key, server_uri=server_url))

# Creating Feeds.
try:
    feed_request = CreateFeedRequest(
        name=FEED_NAME,
        description=FEED_DESCRIPTION,
        platform=PLATFORM,
        workspace=workspace_id,
    )
    created_feed_name = client.create_feed(feed=feed_request).name

    print("Feed created Successfully.")
    print(f"Created feed name: {created_feed_name}")

except ApiException as exp:
    print(exp)
except Exception as exp:
    print(exp)
