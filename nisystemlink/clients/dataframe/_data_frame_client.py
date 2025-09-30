"""Implementation of DataFrameClient."""

from collections.abc import Iterable
from io import BytesIO
from typing import List, Optional, Union

try:
    import pyarrow as pa  # type: ignore
except Exception:
    pa = None
from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import (
    delete,
    get,
    patch,
    post,
    response_handler,
)
from nisystemlink.clients.core.helpers import IteratorFileLike
from requests.models import Response
from uplink import Body, Field, Path, Query, retry

from . import models


# retry for common http status codes and any Connection error
@retry(
    when=retry.when.status([429, 502, 503, 504]),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class DataFrameClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, "/nidataframe/v1/")

    @get("")
    def api_info(self) -> models.ApiInfo:
        """Get information about available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service.
        """
        ...

    @get(
        "tables",
        args=[
            Query("take"),
            Query("id"),
            Query("orderBy"),
            Query("orderByDescending"),
            Query("continuationToken"),
            Query("workspace"),
        ],
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
            The list of tables with a continuation token.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @post("tables", return_key="id")
    def create_table(self, table: models.CreateTableRequest) -> str:
        """Create a new table with the provided metadata and column definitions.

        Args:
            table: The request to create the table.

        Returns:
            The ID of the newly created table.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @post("query-tables")
    def query_tables(self, query: models.QueryTablesRequest) -> models.PagedTables:
        """Queries available tables on the SystemLink DataFrame service and returns their metadata.

        Args:
            query: The request to query tables.

        Returns:
            The list of tables with a continuation token.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @get("tables/{id}")
    def get_table_metadata(self, id: str) -> models.TableMetadata:
        """Retrieves the metadata and column information for a single table identified by its ID.

        Args:
            id (str): Unique ID of a data table.

        Returns:
            The metadata for the table.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @patch("tables/{id}", args=[Path, Body])
    def modify_table(self, id: str, update: models.ModifyTableRequest) -> None:
        """Modify properties of a table or its columns.

        Args:
            id: Unique ID of a data table.
            update: The metadata to update.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @delete("tables/{id}")
    def delete_table(self, id: str) -> None:
        """Deletes a table.

        Args:
            id (str): Unique ID of a data table.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @post("delete-tables", args=[Field("ids")])
    def delete_tables(
        self, ids: List[str]
    ) -> Optional[models.DeleteTablesPartialSuccess]:
        """Deletes multiple tables.

        Args:
            ids (List[str]): List of unique IDs of data tables.

        Returns:
            A partial success if any tables failed to delete, or None if all
            tables were deleted successfully.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
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

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @get(
        "tables/{id}/data",
        args=[
            Path("id"),
            Query("columns"),
            Query("orderBy"),
            Query("orderByDescending"),
            Query("take"),
            Query("continuationToken"),
        ],
    )
    def get_table_data(
        self,
        id: str,
        columns: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        order_by_descending: Optional[bool] = None,
        take: Optional[int] = None,
        continuation_token: Optional[str] = None,
    ) -> models.PagedTableRows:
        """Reads raw data from the table identified by its ID.

        Args:
            id: Unique ID of a data table.
            columns: Columns to include in the response. Data will be returned in the same order as
                the columns. If not specified, all columns are returned.
            order_by: List of columns to sort by. Multiple columns may be specified to order rows
                that have the same value for prior columns. The columns used for ordering do not
                need to be included in the columns list, in which case they are not returned. If
                not specified, then the order in which results are returned is undefined.
            order_by_descending: Whether to sort descending instead of ascending. Defaults to false.
            take: Limits the returned list to the specified number of results. Defaults to 500.
            continuation_token: The token used to paginate results.

        Returns:
            The table data and total number of rows with a continuation token.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @post("tables/{id}/data", args=[Path, Body])
    def _append_table_data_json(
        self, id: str, data: models.AppendTableDataRequest
    ) -> None:
        """Internal uplink-implemented JSON append call."""
        ...

    @post(
        "tables/{id}/data",
        args=[Path, Body, Query("endOfData")],
        content_type="application/vnd.apache.arrow.stream",
    )
    def _append_table_data_arrow(
        self, id: str, data: Iterable[bytes], end_of_data: Optional[bool] = None
    ) -> None:
        """Internal uplink-implemented Arrow (binary) append call."""
        ...

    def append_table_data(
        self,
        id: str,
        data: Optional[
            Union[
                models.AppendTableDataRequest,
                models.DataFrame,
                "pa.RecordBatch",  # type: ignore[name-defined]
                Iterable["pa.RecordBatch"],  # type: ignore[name-defined]
            ]
        ],
        *,
        end_of_data: Optional[bool] = None,
    ) -> None:
        """Appends one or more rows of data to the table identified by its ID.

        Args:
            id: Unique ID of a data table.
            data: The data to append.

                Supported forms:

                * ``AppendTableDataRequest``: Sent as-is via JSON; ``end_of_data`` must be ``None``.
                * ``DataFrame`` (service model): Wrapped into an
                  ``AppendTableDataRequest`` (``end_of_data`` optional) and sent as JSON.
                * Single ``pyarrow.RecordBatch``: Treated the same as an iterable containing one
                  batch and streamed as Arrow IPC. ``end_of_data`` (if provided) is sent as a
                  query parameter.
                * ``Iterable[pyarrow.RecordBatch]``: Streamed as Arrow IPC. ``end_of_data`` (if
                  provided) is sent as a query parameter. If the iterator yields no batches, it is
                  treated as ``None`` and requires ``end_of_data``.
                * ``None``: ``end_of_data`` must be provided; sends JSON containing only the
                  ``endOfData`` flag (useful for closing a table without appending rows).
            end_of_data: Whether additional rows may be appended in future requests. Required when
                ``data`` is ``None`` or the RecordBatch iterator is empty; must be omitted when
                passing an ``AppendTableDataRequest`` (include it inside that model instead).

        Raises:
            ValueError: If parameter constraints are violated.
            ApiException: If unable to communicate with the DataFrame Service or an
                invalid argument is provided.
        """
        if isinstance(data, models.AppendTableDataRequest):
            if end_of_data is not None:
                raise ValueError(
                    "end_of_data must not be provided separately when passing an AppendTableDataRequest."
                )
            self._append_table_data_json(id, data)
            return

        if isinstance(data, models.DataFrame):
            if end_of_data is None:
                request_model = models.AppendTableDataRequest(frame=data)
            else:
                request_model = models.AppendTableDataRequest(
                    frame=data, end_of_data=end_of_data
                )
            self._append_table_data_json(id, request_model)
            return

        if pa is not None and isinstance(data, pa.RecordBatch):
            data = [data]

        if isinstance(data, Iterable):
            iterator = iter(data)
            try:
                first_batch = next(iterator)
            except StopIteration:
                if end_of_data is None:
                    raise ValueError(
                        "end_of_data must be provided when data iterator is empty."
                    )
                self._append_table_data_json(
                    id,
                    models.AppendTableDataRequest(end_of_data=end_of_data),
                )
                return

            if pa is None:
                raise RuntimeError(
                    "pyarrow is not installed. Install to stream RecordBatches."
                )

            if not isinstance(first_batch, pa.RecordBatch):
                raise ValueError(
                    "Iterable provided to data must yield pyarrow.RecordBatch objects."
                )

            def _generate_body() -> Iterable[memoryview]:
                batch = first_batch
                with BytesIO() as buf:
                    options = pa.ipc.IpcWriteOptions(compression="zstd")
                    writer = pa.ipc.new_stream(buf, batch.schema, options=options)

                    while True:
                        writer.write_batch(batch)
                        with buf.getbuffer() as view, view[0 : buf.tell()] as slice:
                            yield slice
                        buf.seek(0)
                        try:
                            batch = next(iterator)
                        except StopIteration:
                            break

                    writer.close()
                    with buf.getbuffer() as view, view[0 : buf.tell()] as slice:
                        yield slice

            try:
                self._append_table_data_arrow(
                    id,
                    _generate_body(),
                    end_of_data,
                )
            except core.ApiException as ex:
                if ex.http_status_code == 400:
                    wrap = True
                    try:
                        write_op = getattr(
                            self.api_info().operations, "write_data", None
                        )
                        if (
                            write_op is not None
                            and getattr(write_op, "version", 0) >= 2
                        ):
                            wrap = False
                    except Exception:
                        pass
                    if wrap:
                        raise core.ApiException(
                            (
                                "Arrow ingestion request was rejected. The target "
                                "DataFrame Service doesn't support Arrow streaming. "
                                "Install a DataFrame Service version with Arrow support "
                                "or fall back to JSON ingestion."
                            ),
                            error=ex.error,
                            http_status_code=ex.http_status_code,
                            inner=ex,
                        ) from ex
                raise
            return

        if data is None:
            if end_of_data is None:
                raise ValueError(
                    "end_of_data must be provided when data is None (no rows to append)."
                )
            self._append_table_data_json(
                id, models.AppendTableDataRequest(end_of_data=end_of_data)
            )
            return

        raise ValueError(
            "Unsupported type for data. Expected AppendTableDataRequest, DataFrame, Iterable[RecordBatch], or None."
        )

    @post("tables/{id}/query-data", args=[Path, Body])
    def query_table_data(
        self, id: str, query: models.QueryTableDataRequest
    ) -> models.PagedTableRows:
        """Reads rows of data that match a filter from the table identified by its ID.

        Args:
            id: Unique ID of a data table.
            query: The filtering and sorting to apply when reading data.

        Returns:
            The table data and total number of rows with a continuation token.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    @post("tables/{id}/query-decimated-data", args=[Path, Body])
    def query_decimated_data(
        self, id: str, query: models.QueryDecimatedDataRequest
    ) -> models.TableRows:
        """Reads decimated rows of data from the table identified by its ID.

        Args:
            id: Unique ID of a data table.
            query: The filtering and decimation options to apply when reading data.

        Returns:
            The decimated table data.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...

    def _iter_content_filelike_wrapper(response: Response) -> IteratorFileLike:
        return IteratorFileLike(response.iter_content(chunk_size=4096))

    @response_handler(_iter_content_filelike_wrapper)
    @post("tables/{id}/export-data", args=[Path, Body])
    def export_table_data(
        self, id: str, query: models.ExportTableDataRequest
    ) -> IteratorFileLike:
        """Exports rows of data that match a filter from the table identified by its ID.

        Args:
            id: Unique ID of a data table.
            query: The filtering, sorting, and export format to apply when exporting data.

        Returns:
            A file-like object for reading the exported data.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service
                or provided an invalid argument.
        """
        ...
