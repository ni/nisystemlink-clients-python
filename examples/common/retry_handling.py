"""Example to handle retry for clients for HTTP status/errors."""

from nisystemlink.clients.core import retry
from nisystemlink.clients.file import FileClient

# Retry on Too Many Requests status or any Exception
WHEN_CLAUSE = retry.when.status(429) | Exception
# Stop after 3 attempts or after the backoff exceeds 10 seconds.
STOP_CLAUSE = retry.stop.after_attempt(3) | retry.stop.after_delay(10)

# Create your Client, this example uses FileClient
_client = FileClient()

# Wrap the client with retry and define the conditions to retry
client: FileClient = retry(
    when=WHEN_CLAUSE,
    stop=STOP_CLAUSE,
)(_client)

# Use the wrapped client as you would use normally
resp = client.get_files()
print(resp.total_count)
