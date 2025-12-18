from nisystemlink.clients.file.models._base_file_request import BaseFileRequest


class SearchFilesRequest(BaseFileRequest):
    """Request model for searching files."""

    order_by: str | None = None
    """
    The name of the metadata field to sort by.
    """
