# TODO: Wrap Uplink decorators to add typing information
# mypy: disable-error-code = misc

"""Implementation of DataFrameClient."""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from uplink import Body, delete, get, json, post, returns

from . import models


class DataFrameClient(BaseClient):
    _BASE_PATH = "/nidataframe/v1"

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`core.JupyterHttpConfiguration` is used.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration)

    @get(_BASE_PATH)
    def api_info(self) -> models.ApiInfo:
        """Returns information about available API operations."""
        ...

    @json
    @returns.json(key="id")
    @post(_BASE_PATH + "/tables", args=(Body,))
    def create_table(self, table: models.CreateTableRequest) -> str:
        """Create a new table with the provided metadata and column definitions.

        Args:
            table: The request create the table.

        Returns:
            The ID of the newly created table.
        """
        ...

    @get(_BASE_PATH + "/tables/{id}")
    def get_table_metadata(self, id: str) -> models.TableMetadata:
        """Retrieves the metadata and column information for a single table identified by its ID.

        Args:
            id (str): Unique ID of a DataFrame table.

        Returns:
            models.TableMetadata: The metadata for the table.
        """
        ...

    @delete(_BASE_PATH + "/tables/{id}")
    def delete_table(self, id: str) -> None:
        """Deletes a table.

        Args:
            id (str): Unique ID of a DataFrame table.
        """
        ...
