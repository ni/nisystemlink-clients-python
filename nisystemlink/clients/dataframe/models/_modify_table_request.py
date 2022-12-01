from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._table_metadata_modification_base import TableMetdataModificationBase


class ColumnMetadataPatch(JsonModel):
    """Specifies column properties to add, modify, or delete when editing table metadata."""

    name: str
    """The name of the column to modify."""

    properties: Dict[str, Optional[str]]
    """The properties to modify. A map of key value properties containing the metadata
    to be added or modified. Setting a property value to ``None`` will delete the
    property."""


class ModifyTableRequest(TableMetdataModificationBase):
    """Contains the metadata properties to modify. Values not included will remain unchanged."""

    columns: Optional[List[ColumnMetadataPatch]] = None
    """Updates to the column properties. Cannot add or remove columns, or change the name of a column."""
