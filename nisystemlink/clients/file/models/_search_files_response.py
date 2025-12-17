from datetime import datetime
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._file_linq_query import TotalCount
from ._file_metadata import BaseFileMetadata


class SearchFileMetadata(BaseFileMetadata):
    """File metadata returned from search files operation."""

    user_id: str | None = None
    """
    The ID of the user who created the file.
    """

    org_id: str | None = None
    """
    The organization ID that owns the file.
    """

    name: str | None = None
    """
    The name of the file.
    """

    content_type: str | None = None
    """
    The content type of the file.
    """

    updated: datetime | None = None
    """
    The date and time the file was last updated.
    """

    deleted: bool | None = None
    """
    Whether the file has been deleted.
    """

    encryption_schema: int | None = None
    """
    The encryption schema used for the file.
    """

    download_key: str | None = None
    """
    The key used to download the file.
    """

    chunks: int | None = None
    """
    The number of chunks in the file.
    """


class SearchFilesResponse(JsonModel):
    """Response model for search files operation."""

    available_files: List[SearchFileMetadata] | None = None
    """
    List of files matching the search criteria.
    """

    total_count: TotalCount | None = None
    """
    Total number of files matching the search criteria.
    """
