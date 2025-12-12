"""Example to demonstrate reading the minion ID from the Salt configuration."""

from nisystemlink.clients.core.helpers import read_minion_id

# Read the minion ID from the Salt configuration file
minion_id = read_minion_id()

if minion_id:
    print(f"Minion ID: {minion_id}")
else:
    print("Minion ID not found. Please ensure the SystemLink client is connected to the Server.")
