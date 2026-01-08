"""Example demonstrating the paginate helper for iterating through paginated API results.

This example shows how to use the paginate() helper function to automatically
handle continuation tokens when fetching all results from a paginated API.
"""

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.core.helpers import paginate
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import Result

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = TestMonitorClient(configuration=server_configuration)

# Example 1: Basic usage - iterate through all results automatically
print("Example 1: Iterating through all results")
print("-" * 50)
result: Result
for result in paginate(client.get_results, items_field="results", take=100):
    print(f"Result ID: {result.id}, Status: {result.status.status_type}")  # type: ignore[union-attr]

# Example 2: Collect all results into a list
print("\nExample 2: Collecting all results into a list")
print("-" * 50)
all_results: list[Result] = list(
    paginate(client.get_results, items_field="results", take=100)
)
print(f"Total results retrieved: {len(all_results)}")

# Example 3: Process in chunks while still using automatic pagination
print("\nExample 3: Processing results in batches")
print("-" * 50)
batch: list[Result] = []
batch_size = 50
for i, result in enumerate(
    paginate(client.get_results, items_field="results", take=100), start=1
):
    batch.append(result)
    if len(batch) >= batch_size:
        # Process batch
        print(f"Processing batch of {len(batch)} results...")
        # Do something with batch
        batch = []

# Process remaining items
if batch:
    print(f"Processing final batch of {len(batch)} results...")
