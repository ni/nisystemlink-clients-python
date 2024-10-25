"""Functionality of deleting feed API."""

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds._feeds_client import FeedsClient


FEED_ID = ""

server_url = ""  # SystemLink API URL
server_api_key = ""  # SystemLink API key

# Please provide the valid API key and API URL for client intialization.
client = FeedsClient(HttpConfiguration(api_key=server_api_key, server_uri=server_url))

# Deleting Feed.
try:
    created_feed_name = client.delete_feed(id=FEED_ID)
    print("Feed deleted successfully.")

except ApiException as exp:
    print(exp)
except Exception as exp:
    print(exp)
