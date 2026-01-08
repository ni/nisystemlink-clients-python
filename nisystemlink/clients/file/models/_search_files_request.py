from nisystemlink.clients.file.models._base_file_request import BaseFileRequest
from nisystemlink.clients.file.models._file_query_order_by import SearchFilesOrderBy


class SearchFilesRequest(BaseFileRequest):
    """Request model for searching files."""

    filter: str | None = None
    """
    The filter criteria for files using Lucene query syntax. Consists of a string of queries composed
    using AND/OR operators. String values and date strings need to be enclosed in double quotes.
    Parentheses can be used around filters to better define the order of operations.
    Example Filter syntax: '[property name]:[operand] AND [property name]:[operand]'
    """

    order_by: SearchFilesOrderBy | None = None
    """
    The property by which to order the files in the response.
    """
