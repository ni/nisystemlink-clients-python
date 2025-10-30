from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._column import Column


class CreateTableRequest(JsonModel):
    """Contains information needed to create a table, including its properties and column definitions."""

    columns: List[Column]
    """The list of columns in the table. Exactly one column must have a :class:`.ColumnType` of INDEX."""

    name: Optional[str] = None
    """The name to associate with the table. When not specified, a name will be
    assigned from the table's ID."""

    properties: Optional[Dict[str, str]] = None
    """User-defined properties to associate with the table."""

    test_result_id: Optional[str] = None
    """The ID of the test result associated with the table. A value of ``None`` or an empty string
    indicates there is no associated test result. Added in version 2 of the
    :py:attr:`nisystemlink.clients.dataframe.models.OperationsV1.create_tables` operation. Older
    versions of the service will ignore this value."""

    workspace: Optional[str] = None
    """The workspace to create the table in. Uses the default workspace when not specified."""
