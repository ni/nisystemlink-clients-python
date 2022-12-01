from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._table_metadata_modification_base import TableMetdataModificationBase


class TableMetdataModification(TableMetdataModificationBase):
    """Contains the metadata properties to modify. Values not included will remain unchanged."""

    id: str
    """The ID of the table to modify."""


class ModifyTablesRequest(JsonModel):
    """Contains one or more table modifications to apply."""

    tables: List[TableMetdataModification]
    """The table modifications to apply. Each table may only appear once in the list."""

    replace: bool
    """When true, existing properties are replaced instead of merged."""
