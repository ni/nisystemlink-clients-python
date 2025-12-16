"""Example demonstrating how to search for files using the File API."""

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.file import FileClient, models

# Configure connection to SystemLink server
server_configuration = HttpConfiguration(
    server_uri="https://your-server-url.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)

client = FileClient(configuration=server_configuration)

# Example 1: Basic file search with filter
print("Example 1: Search files with filter")
search_request = models.SearchFilesRequest(
    filter='name:("myfile.txt")',
    skip=0,
    take=10,
)

response = client.search_files(search_request)
print(f"Found {response.total_count} file(s) matching the filter")
if response.available_files:
    for file in response.available_files:
        print(f"  - {file.name} (ID: {file.id}, Size: {file.size} bytes)")

# Example 2: Search with pagination and sorting
print("\nExample 2: Search with pagination and sorting")
search_request = models.SearchFilesRequest(
    filter='size:([1000 TO *])',
    skip=0,
    take=20,
    order_by="created",
    order_by_descending=True,
)

response = client.search_files(search_request)
print(f"Found {response.total_count} file(s) larger than 1000 bytes")
if response.available_files:
    for file in response.available_files:
        print(
            f"  - {file.name} created at {file.created} (Size: {file.size} bytes)"
        )

# Example 3: Search files in a specific workspace
print("\nExample 3: Search files in a specific workspace")
search_request = models.SearchFilesRequest(
    filter='workspace:("my-workspace-id")',
    skip=0,
    take=10,
)

response = client.search_files(search_request)
print(f"Found {response.total_count} file(s) in the workspace")
if response.available_files:
    for file in response.available_files:
        print(f"  - {file.name} in workspace {file.workspace}")

# Example 4: Search by content type
print("\nExample 4: Search by content type")
search_request = models.SearchFilesRequest(
    filter='contentType:("application/json")',
    skip=0,
    take=10,
    order_by="name",
    order_by_descending=False,
)

response = client.search_files(search_request)
print(f"Found {response.total_count} JSON file(s)")
if response.available_files:
    for file in response.available_files:
        print(f"  - {file.name} ({file.content_type})")
