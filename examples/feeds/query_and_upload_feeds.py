"""Functionality of uploading & querying feeds APIs."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient
from nisystemlink.clients.feeds.models import Platform
from nisystemlink.clients.feeds.utilities import get_feed_by_name

# Update the constants.
FEED_NAME = ""
PLATFORM = None
FEED_DESCRIPTION = ""
PLATFORM = Platform.WINDOWS
WORKSPACE_ID = (
    None # None uses Default workspace. Replace with Systemlink workspace id.
)
PACKAGE_PATH = ""

server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key

# Provide the valid API key and API URL for client intialization.
client = FeedsClient(HttpConfiguration(api_key=server_api_key, server_uri=server_url))

# To upload a package to feed.
try:
    # Get ID of the Feed to upload by name
    feeds = client.query_feeds(platform=PLATFORM, workspace=WORKSPACE_ID)
    feed = get_feed_by_name(feeds=feeds, name=FEED_NAME)
    feed_id = feed.id if feed else None

    # Upload the package to Feed by ID
    if feed_id:
        client.upload_package(
            feed_id=feed_id,
            overwrite=True,
            package_file_path=PACKAGE_PATH,
        )
        print("Package uploaded sucessfully.")

except ApiException as exp:
    print(exp)

except Exception as exp:
    print(exp)
