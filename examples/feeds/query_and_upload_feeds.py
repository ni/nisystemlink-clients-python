"""Functionality of uploading & querying feeds APIs."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient
from nisystemlink.clients.feeds.models import Platform
from nisystemlink.clients.feeds.utilities import get_feed_id

# Constant
FEED_NAME = "EXAMPLE FEED"
FEED_DESCRIPTION = "EXAMPLE DESCRIPTION"
PLATFORM = Platform.WINDOWS
PACKAGE_NAME = ""
PACKAGE_PATH = ""

server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key
workspace_id = ""  # Systemlink workspace id

# Please provide the valid API key and API URL for client intialization.
client = FeedsClient(HttpConfiguration(api_key=server_api_key, server_uri=server_url))

# To upload a package to feed.
try:
    # To query available feeds.
    query_feeds_response = client.query_feeds(
        platform=PLATFORM,
        workspace=workspace_id,
    )

    feed_id = get_feed_id(feeds_details=query_feeds_response.feeds, feed_name=FEED_NAME)

    if feed_id:
        upload_package = client.upload_package(
            feed_id=feed_id,
            overwrite=True,
            package=open(PACKAGE_PATH, "rb"),
        )
        print("Package uploaded sucessfully.")

except ApiException as exp:
    print(exp)

except Exception as exp:
    print(exp)
