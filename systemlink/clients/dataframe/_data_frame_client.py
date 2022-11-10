# TODO: Wrap Uplink decorators to add typing information
# mypy: disable-error-code = misc

"""Implementation of DataFrameClient."""

from typing import Any

from systemlink.clients.core._uplink._base_client import BaseClient
from uplink import get, returns


class DataFrameClient(BaseClient):
    @returns.json()
    @get("nidataframe")
    # TODO: Create model class for return type
    def api_info(self) -> dict:
        """Returns information about API versions and available operations."""
        pass
