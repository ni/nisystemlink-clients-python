from typing import BinaryIO, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._file_like_response import (
    file_like_response_handler,
)
from nisystemlink.clients.core._uplink._methods import (
    delete,
    get,
    post,
    put,
    response_handler,
)
from nisystemlink.clients.core.helpers._iterator_file_like import IteratorFileLike
from uplink import Part, Path

from . import models


class NotebookClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Notebook Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()
        super().__init__(configuration, base_path="/ninotebook/v1/")

    @get("notebook/{id}")
    def get_notebook(self, id: str) -> models.NotebookMetadata:
        """Gets a notebook metadata by ID.

        Args:
            id: The ID of the notebook to read.

        Returns:
            The notebook metadata.

        Raises:
            ApiException: if unable to communicate with the Notebook service or provided invalid
                arguments.
        """
        ...

    @put("notebook/{id}", args=[Path("id"), Part("metadata"), Part("content")])
    def update_notebook(
        self,
        id: str,
        metadata: Optional[models.NotebookMetadata] = None,
        content: Optional[BinaryIO] = None,
    ) -> models.NotebookMetadata:
        """Updates a notebook metadata by ID.

        Args:
            id: The ID of the notebook to update.
            metadata: The notebook metadata.
            content: The notebook binary content.

        Returns:
            The updated notebook metadata.

        Raises:
            ApiException: if unable to communicate with the Notebook service or provided invalid
                arguments.
        """
        ...

    @delete("notebook/{id}")
    def delete_notebook(self, id: str) -> None:
        """Deletes a notebook by ID.

        Args:
            id: The ID of the notebook to delete.

        Raises:
            ApiException: if unable to communicate with the Notebook service or provided invalid
                arguments.
        """
        ...

    @post("notebook", args=[Part("metadata"), Part("content")])
    def create_notebook(
        self,
        metadata: models.NotebookMetadata,
        content: BinaryIO,
    ) -> models.NotebookMetadata:
        """Creates a new notebook.

        Args:
            metadata: The notebook metadata.
            content: The notebook binary content.

        Returns:
            The created notebook metadata.

        Raises:
            ApiException: if unable to communicate with the Notebook service or provided invalid
                arguments.
        """
        ...

    @post("notebook/{id}/query")
    def query_notebook(
        self, query: models.QueryNotebookRequest
    ) -> models.QueryNotebookResponse:
        """Queries notebooks.

        Args:
            query: The query parameters.

        Returns:
            The paged notebooks.

        Raises:
            ApiException: if unable to communicate with the Notebook service or provided invalid
                arguments.
        """
        ...

    @response_handler(file_like_response_handler)
    @get("notebook/{id}/content")
    def get_notebook_content(self, id: str) -> IteratorFileLike:
        """Gets a notebook content by ID.

        Args:
            id: The ID of the notebook to read.

        Returns:
            A file-like object for reading the notebook content.

        Raises:
            ApiException: if unable to communicate with the Notebook service or provided invalid
                arguments.
        """
        ...
