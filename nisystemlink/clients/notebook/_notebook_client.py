import io
from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._api_error import ApiError
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
from uplink import Part, Path, retry

from . import models


@retry(when=retry.when.status(429), stop=retry.stop.after_attempt(5))
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
        super().__init__(configuration, base_path="/")

    @get("ninotebook/v1/notebook/{id}")
    def get_notebook(self, id: str) -> models.NotebookMetadata:
        """Gets a notebook metadata by ID.

        Args:
            id: The ID of the notebook to read.

        Returns:
            The notebook metadata.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        ...

    @put("ninotebook/v1/notebook/{id}")
    def __update_notebook(
        self,
        id: Path,
        metadata: Part = None,
        content: Part = None,
    ) -> models.NotebookMetadata:
        """Updates a notebook metadata by ID.

        Args:
            id: The ID of the notebook to update.
            metadata: The notebook metadata.
            content: The notebook binary content.

        Returns:
            The updated notebook metadata.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        ...

    def update_notebook(
        self,
        id: str,
        metadata: Optional[models.NotebookMetadata] = None,
        content: Optional[io.BufferedReader] = None,
    ) -> models.NotebookMetadata:
        """Updates a notebook metadata by ID.

        Args:
            id: The ID of the notebook to update.
            metadata: The notebook metadata.
            content: The notebook binary content.

        Returns:
            The updated notebook metadata.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        metadata_io = None
        if metadata is not None:
            metadata_str = metadata.model_dump_json(by_alias=True, exclude_unset=True)
            metadata_io = io.BytesIO(metadata_str.encode("utf-8"))

        return self.__update_notebook(
            id=id,
            metadata=metadata_io,
            content=content,
        )

    @delete("ninotebook/v1/notebook/{id}")
    def delete_notebook(self, id: str) -> None:
        """Deletes a notebook by ID.

        Args:
            id: The ID of the notebook to delete.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        ...

    @post("ninotebook/v1/notebook")
    def __create_notebook(
        self,
        metadata: Part,
        content: Part,
    ) -> models.NotebookMetadata:
        """Creates a new notebook.

        Args:
            metadata: The notebook metadata.
            content: The notebook binary content.

        Returns:
            The created notebook metadata.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        ...

    def create_notebook(
        self,
        metadata: models.NotebookMetadata,
        content: io.BufferedReader,
    ) -> models.NotebookMetadata:
        """Creates a new notebook.

        Args:
            metadata: The notebook metadata.
            content: The notebook binary content.

        Returns:
            The created notebook metadata.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        metadata_str = metadata.model_dump_json()

        metadata_io = io.BytesIO(metadata_str.encode("utf-8"))
        return self.__create_notebook(
            metadata=metadata_io,
            content=content,
        )

    @post("ninotebook/v1/notebook/query")
    def query_notebooks(
        self, query: models.QueryNotebookRequest
    ) -> models.PagedNotebooks:
        """Queries notebooks.

        Args:
            query: The query parameters.

        Returns:
            The paged notebooks.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        ...

    @response_handler(file_like_response_handler)
    @get("ninotebook/v1/notebook/{id}/content")
    def get_notebook_content(self, id: str) -> IteratorFileLike:
        """Gets a notebook content by ID.

        Args:
            id: The ID of the notebook to read.

        Returns:
            A file-like object for reading the notebook content.

        Raises:
            ApiException: if unable to communicate with the ``/ninotebook`` service or provided invalid
                arguments.
        """
        ...

    @post("ninbexecution/v1/executions")
    def create_executions(
        self, executions: List[models.CreateExecutionRequest]
    ) -> models.CreateExecutionsResponse:
        """Create one or more executions of Jupyter notebooks.

        Args:
            execution: information about an execution of a Jupyter notebook.

        Returns:
            A response to a request to create executions.

        Raises:
            ApiException: if unable to communicate with the ``/ninbexecution`` Service
                or provided an invalid argument.
        """
        ...

    @get("ninbexecution/v1/executions/{id}")
    def get_execution_by_id(self, id: str) -> models.Execution:
        """Get information about the specified execution of a Jupyter notebook.

        Args:
            id: the ID of the execution.

        Returns:
            Information about the execution of a Jupyter notebook fetched using it's Id.

        Raises:
            ApiException: if unable to communicate with the ``/ninbexecution`` Service
                or provided an invalid argument.
        """
        ...

    @post("ninbexecution/v1/query-executions")
    def __query_executions(
        self, query: models._QueryExecutionsRequest
    ) -> List[models.Execution]:
        """Query executions of Jupyter notebooks.

        Args:
            query: query for executions of Jupyter notebooks.

        Returns:
            A response to a request to query executions.

        Raises:
            ApiException: if unable to communicate with the ``/ninbexecution`` Service
                or provided an invalid argument.
        """
        ...

    def query_executions(
        self, query: models.QueryExecutionsRequest
    ) -> List[models.Execution]:
        """Query executions of Jupyter notebooks.

        Args:
            query: query for executions of Jupyter notebooks.

        Returns:
            A response to a request to query executions.

        Raises:
            ApiException: if unable to communicate with the ``/ninbexecution`` Service
                or provided an invalid argument.
        """
        projection = ",".join(query.projection)
        projection_str = f"new({projection})" if projection else None

        query_params = {
            "filter": query.filter,
            "order_by": query.order_by,
            "descending": query.descending,
            "projection": projection_str,
        }

        query_params = {k: v for k, v in query_params.items() if v is not None}

        query_request = models._QueryExecutionsRequest(**query_params)

        return self.__query_executions(query=query_request)

    @post("ninbexecution/v1/retry-executions", return_key="error")
    def retry_executions(self, ids: List[str]) -> Optional[ApiError]:
        """Retries existing executions based on failed, canceled or timed-out executions.

        Args:
            ids: List of execution IDs to retry.

        Returns:
            An ApiError object if executions could not be retried.
            None if executions were retried successfully.

        Raises:
            ApiException: if unable to communicate with the ``/ninbexecution`` Service
                or provided an invalid argument.
        """
        ...

    @post("ninbexecution/v1/cancel-executions", return_key="error")
    def cancel_executions(self, ids: List[str]) -> Optional[ApiError]:
        """Cancel queued and in-progress executions.

        Args:
            ids: List of execution IDs to cancel.

        Returns:
            An ApiError object if executions could not be canceled.
            None if executions were canceled successfully.

        Raises:
            ApiException: if unable to communicate with the ``/ninbexecution`` Service
                or provided an invalid argument.
        """
        ...

    @post("ninbexecution/v1/create-executions-from-existing")
    def create_executions_from_existing(
        self, ids: List[str]
    ) -> models.CreateExecutionsResponse:
        """Create new executions based on already existing succeeded executions.

        Args:
            ids: List of execution IDs to run again.

        Returns:
            A response to a request to create executions.

        Raises:
            ApiException: if unable to communicate with the ``/ninbexecution`` Service
                or provided an invalid argument.
        """
        ...
