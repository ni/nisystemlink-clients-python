"""Functionality of uploading & querying feeds APIs."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient
from nisystemlink.clients.feeds.models import Platform
from nisystemlink.clients.feeds.utilities._get_feed_details import get_feed_by_name

# Update the constants.
FEED_NAME = ""
PLATFORM = None
FEED_DESCRIPTION = ""
PLATFORM = Platform.WINDOWS
WORKSPACE_ID = (
    None  # None uses Default workspace. Replace with Systemlink workspace id.
)
PACKAGE_PATH = ""

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = FeedsClient(configuration=server_configuration)

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
