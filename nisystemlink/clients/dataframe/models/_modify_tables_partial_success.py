from typing import List

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._modify_tables_request import TableMetdataModification


class ModifyTablesPartialSuccess(JsonModel):
    """The result of modifying multiple tables when one or more tables could not be modified."""

    modified_table_ids: List[str]
    """The IDs of the tables that were successfully modified."""

    failed_modifications: List[TableMetdataModification]
    """The requested modifications that could not be applied."""

    error: ApiError
    """The error that occurred when modifying the tables."""
