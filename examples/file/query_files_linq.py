"""Example to query files using LINQ filters in SystemLink."""

from nisystemlink.clients.file import FileClient
from nisystemlink.clients.file.models import FileLinqQueryOrderBy, FileLinqQueryRequest

client = FileClient()


# Example 1: Basic query to find files by name
query_request = FileLinqQueryRequest(filter='name == "example_file.txt"')
response = client.query_files_linq(query=query_request)

print(f"Found {response.total_count.value} files matching the filter")
for file in response.available_files:
    file_name = file.properties.get("Name", "Unknown") if file.properties else "Unknown"
    print(f"- File ID: {file.id}, Name: {file_name}")


# Example 2: Query with ordering and pagination
query_request = FileLinqQueryRequest(
    filter='name.Contains("test")',  # Find files with "test" in the name
    order_by=FileLinqQueryOrderBy.CREATED,
    order_by_descending=True,  # Most recent first
    take=5,  # Limit to 5 results
)
response = client.query_files_linq(query=query_request)

print(
    f"\nFound {len(response.available_files)} files (limited to {query_request.take}) with 'test' in name"
)
for file in response.available_files:
    file_name = file.properties.get("Name", "Unknown") if file.properties else "Unknown"
    print(f"- File ID: {file.id}, Name: {file_name}")
    print(f"  Created: {file.created}")


# Example 3: Query files by size
query_request = FileLinqQueryRequest(
    filter="size > 1024",  # Files larger than 1KB
    order_by=FileLinqQueryOrderBy.SIZE,
    order_by_descending=True,  # Largest first
    take=3,
)
response = client.query_files_linq(query=query_request)

print(
    f"\nFound {len(response.available_files)} files (limited to {query_request.take}) larger than 1KB"
)
for file in response.available_files:
    file_name = file.properties.get("Name", "Unknown") if file.properties else "Unknown"
    print(f"- File ID: {file.id}, Name: {file_name}")
    print(f"  Size: {file.size} bytes")
