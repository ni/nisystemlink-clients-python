"""Functionality of uploading & querying feeds APIs."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds.feeds_client import SystemLinkFeedsClient
from nisystemlink.clients.feeds.models import Platform


# Constant
FEED_NAME = "EXAMPLE FEED"
FEED_DESCRIPTION = "EXAMPLE DESCRIPTION"
PLATFORM = Platform.WINDOWS.value
PACKAGE_NAME = ""
PACKAGE_PATH = ""

server_url = None # SystemLink API URL
server_api_key = None # SystemLink API key
workspace_id = None # Systemlink workspace id

# Please provide the valid API key and API URL for client intialization.
client = SystemLinkFeedsClient(HttpConfiguration(api_key=server_api_key, server_uri=server_url))

# To upload a package to feed.
try:
    # To query available feeds.
    query_feeds = client.query_feeds(
        platform=PLATFORM,
        workspace=workspace_id,
    )
    existing_feeds = {}
    feed_id = ""
    for feed in query_feeds.feeds:
        if feed.name == FEED_NAME:
            feed_id = feed.id
            break

    upload_package = client.upload_package(
        feed_id=feed_id,
        overwrite=True,
        package=(PACKAGE_NAME, open(PACKAGE_PATH, "rb"), "multipart/form-data"),
    )
    print("Package uploaded sucessfully.")
    print(f"Upload package: {upload_package.metadata.package_name}")

except ApiException as exp:
    print(exp)

except Exception as exp:
    print(exp)
