from typing import List

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteTablesPartialSuccess(JsonModel):
    """The result of deleting multiple tables when one or more tables could not be deleted."""

    deleted_table_ids: List[str]
    """The IDs of the tables that were successfully deleted."""

    failed_table_ids: List[str]
    """The IDs of the tables that could not be deleted."""

    error: ApiError
    """The error that occurred when deleting the tables."""
