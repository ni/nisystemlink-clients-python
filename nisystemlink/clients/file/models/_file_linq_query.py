from nisystemlink.clients.file.models._base_file_request import BaseFileRequest
from nisystemlink.clients.file.models._base_file_response import BaseFileResponse
from nisystemlink.clients.file.models._file_query_order_by import FileLinqQueryOrderBy


class FileLinqQueryRequest(BaseFileRequest):
    """Request model for LINQ query operations."""

    filter: str | None = None
    """
    The filter criteria for files. Consists of a string of queries composed using AND/OR operators.
    String values and date strings need to be enclosed in double quotes. Parentheses can be used
    around filters to better define the order of operations.
    Example Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'
    """

    order_by: FileLinqQueryOrderBy | None = None
    """
    The property by which to order the files in the response.
    """


class FileLinqQueryResponse(BaseFileResponse):
    """Response model for LINQ query operations."""

    pass
