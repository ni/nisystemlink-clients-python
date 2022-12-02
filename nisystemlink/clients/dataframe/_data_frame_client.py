"""Implementation of DataFrameClient."""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, patch, post
from uplink import Body, Field, Path, Query

from . import models


class DataFrameClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`core.JupyterHttpConfiguration` is used.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, "/nidataframe/v1/")

    @get("")
    def api_info(self) -> models.ApiInfo:
        """Returns information about available API operations."""
        ...

    @get(
        "tables",
        args=(
            Query("take"),
            Query("id"),
            Query("orderBy"),
            Query("orderByDescending"),
            Query("continuationToken"),
            Query("workspace"),
        ),
    )
    def list_tables(
        self,
        take: Optional[int] = None,
        id: Optional[List[str]] = None,
        order_by: Optional[models.OrderBy] = None,
        order_by_descending: Optional[bool] = None,
        continuation_token: Optional[str] = None,
        workspace: Optional[List[str]] = None,
    ) -> models.PagedTables:
        """Lists available tables on the SystemLink DataFrame service.

        Args:
            take: Limits the returned list to the specified number of results. Defaults to 1000.
            id: List of table IDs to filter by.
            order_by: The sort order of the returned list of tables.
            order_by_descending: Whether to sort descending instead of ascending. Defaults to false.
            continuation_token: The token used to paginate results.
            workspace: List of workspace IDs to filter by.

        Returns:
            models.PagedTables: The list of tables with a continuation token.
        """
        ...

    @post("tables", return_key="id")
    def create_table(self, table: models.CreateTableRequest) -> str:
        """Create a new table with the provided metadata and column definitions.

        Args:
            table: The request to create the table.

        Returns:
            The ID of the newly created table.
        """
        ...

    @post("query-tables")
    def query_tables(self, query: models.QueryTablesRequest) -> models.PagedTables:
        """Queries available tables on the SystemLink DataFrame service and returns their metadata.

        Args:
            query: The request to query tables.

        Returns:
            models.PagedTables: The list of tables with a continuation token.
        """
        ...

    @get("tables/{id}")
    def get_table_metadata(self, id: str) -> models.TableMetadata:
        """Retrieves the metadata and column information for a single table identified by its ID.

        Args:
            id (str): Unique ID of a DataFrame table.

        Returns:
            models.TableMetadata: The metadata for the table.
        """
        ...

    @patch("tables/{id}", args=[Path, Body])
    def modify_table(self, id: str, update: models.ModifyTableRequest) -> None:
        """Modify properties of a table or its columns.

        Args:
            id: Unique ID of a DataFrame table.
            update: The metadata to update.
        """
        ...

    @delete("tables/{id}")
    def delete_table(self, id: str) -> None:
        """Deletes a table.

        Args:
            id (str): Unique ID of a DataFrame table.
        """
        ...

    @post("delete-tables", args=[Field("ids")])
    def delete_tables(
        self, ids: List[str]
    ) -> Optional[models.DeleteTablesPartialSuccess]:
        """Deletes multiple tables.

        Args:
            ids (List[str]): List of unique IDs of DataFrame tables.

        Returns:
            A partial success if any tables failed to delete, or None if all
            tables were deleted successfully.
        """
        ...

    @post("modify-tables")
    def modify_tables(
        self, updates: models.ModifyTablesRequest
    ) -> Optional[models.ModifyTablesPartialSuccess]:
        """Modify the properties associated with the tables identified by their IDs.

        Args:
            updates: The table modifications to apply.

        Returns:
            A partial success if any tables failed to be modified, or None if all
            tables were modified successfully.
        """
        ...
