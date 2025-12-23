from nisystemlink.clients.file.models._base_file_request import BaseFileRequest
from nisystemlink.clients.file.models._file_query_order_by import SearchFilesOrderBy


class SearchFilesRequest(BaseFileRequest):
    """Request model for searching files."""

    order_by: SearchFilesOrderBy | None = None
    """
    The property by which to order the files in the response.
    """
