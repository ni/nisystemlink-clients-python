"""Example demonstrating how to search for files using the File API."""

import io
import time

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.file import FileClient, models

# Configure connection to SystemLink server
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)

client = FileClient(configuration=server_configuration)

# Upload a test file first
print("Uploading test file...")
test_file_content = b"This is a test file for search demonstration."
test_file = io.BytesIO(test_file_content)
test_file.name = "search-example-test-file.txt"

file_id = client.upload_file(file=test_file)
print(f"Uploaded test file with ID: {file_id}")

# Wait for the file to be indexed for search
# Note: Files may take a few seconds to appear in search results after upload
print("Waiting 5 seconds for file to be indexed for search...")
time.sleep(5)
print()

# Example 1: Basic file search with filter - search for the uploaded file
print("Example 1: Search for the uploaded test file")
search_request = models.SearchFilesRequest(
    filter='name:("search-example-test-file.txt")',
    skip=0,
    take=10,
)

response = client.search_files(search_request)
print(
    f"Found {response.total_count.value if response.total_count else 0} file(s) matching the filter"
)
if response.available_files:
    for file in response.available_files:
        if file.properties:
            print(
                f"- {file.properties.get('Name')} (ID: {file.id}, Size: {file.size} bytes)"
            )

# Example 2: Search with wildcard pattern
print("\nExample 2: Search with wildcard pattern")
search_request = models.SearchFilesRequest(
    filter='name:("search-example*")',
    skip=0,
    take=20,
    order_by="created",
    order_by_descending=True,
)

response = client.search_files(search_request)
print(
    f"Found {response.total_count.value if response.total_count else 0} file(s) starting with 'search-example'"
)
if response.available_files:
    for file in response.available_files:
        if file.properties:
            print(
                f"- {file.properties.get('Name')} created at {file.created} (Size: {file.size} bytes)"
            )

# Example 3: Search by size range
print("\nExample 3: Search by size range")
search_request = models.SearchFilesRequest(
    filter="size:([1 TO 1000])",
    skip=0,
    take=10,
)

response = client.search_files(search_request)
print(
    f"Found {response.total_count.value if response.total_count else 0} file(s) between 1 and 1000 bytes"
)
if response.available_files:
    for file in response.available_files:
        if file.properties:
            print(f"- {file.properties.get('Name')} (Size: {file.size} bytes)")

# Clean up: delete the test file
print("\nCleaning up...")
client.delete_file(id=file_id)
print(f"Deleted test file with ID: {file_id}")
