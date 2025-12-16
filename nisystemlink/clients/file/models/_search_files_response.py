from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._file_linq_query import TotalCount


class SearchFileMetadata(JsonModel):
    """File metadata returned from search files operation."""

    id: Optional[str] = None
    """
    The file's unique identifier.
    """

    user_id: Optional[str] = None
    """
    The ID of the user who created the file.
    """

    org_id: Optional[str] = None
    """
    The organization ID that owns the file.
    """

    service_group: Optional[str] = None
    """
    The service group that owns the file.
    """

    name: Optional[str] = None
    """
    The name of the file.
    """

    created: Optional[datetime] = None
    """
    The date and time the file was created.
    """

    size: Optional[int] = None
    """
    The file size in bytes.
    """

    content_type: Optional[str] = None
    """
    The content type of the file.
    """

    properties: Optional[Dict[str, str]] = None
    """
    The file's properties as key-value pairs.
    """

    updated: Optional[datetime] = None
    """
    The date and time the file was last updated.
    """

    deleted: Optional[bool] = None
    """
    Whether the file has been deleted.
    """

    encryption_schema: Optional[int] = None
    """
    The encryption schema used for the file.
    """

    download_key: Optional[str] = None
    """
    The key used to download the file.
    """

    chunks: Optional[int] = None
    """
    The number of chunks in the file.
    """

    workspace: Optional[str] = None
    """
    The workspace the file belongs to.
    """


class SearchFilesResponse(JsonModel):
    """Response model for search files operation."""

    available_files: Optional[List[SearchFileMetadata]] = None
    """
    List of files matching the search criteria.
    """

    total_count: Optional[TotalCount] = None
    """
    Total number of files matching the search criteria.
    """
