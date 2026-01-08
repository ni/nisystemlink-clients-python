"""Functionality of creating feeds APIs."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds import FeedsClient
from nisystemlink.clients.feeds.models import (
    CreateFeedRequest,
    Platform,
)

# Update the constants.
FEED_NAME = ""
FEED_DESCRIPTION = ""
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

# Creating Feeds.
try:
    feed_request = CreateFeedRequest(
        name=FEED_NAME,
        description=FEED_DESCRIPTION,
        platform=PLATFORM,
        workspace=WORKSPACE_ID,
    )
    feed_details = client.create_feed(feed=feed_request)

    print("Feed created Successfully.")
    print(f"Created feed details: {feed_details}")

except ApiException as exp:
    print(exp)
except Exception as exp:
    print(exp)
