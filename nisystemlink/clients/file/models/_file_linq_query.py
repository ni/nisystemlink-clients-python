from nisystemlink.clients.file.models._base_file_request import BaseFileRequest
from nisystemlink.clients.file.models._base_file_response import BaseFileResponse
from nisystemlink.clients.file.models._file_query_order_by import FileLinqQueryOrderBy


class FileLinqQueryRequest(BaseFileRequest):
    order_by: FileLinqQueryOrderBy | None = None
    """The property by which to order the files in the response."""


class FileLinqQueryResponse(BaseFileResponse):
    """Response model for LINQ query operations."""

    pass
