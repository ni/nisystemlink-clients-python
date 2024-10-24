from __future__ import annotations

from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._file_metadata import FileMetadata
from ._link import Link


class FileQueryResponse(JsonModel):
    """The result of a file query"""

    field_links: Dict[str, Link] = Field(alias="_links")
    """The links that apply to the collection of files for a service group:
    - deleteFiles: Link to delete multiple files from the service group using a POST
    - query: Link to query for available files in the service group using a POST
    - search: Link to retrieve a filtered list of files in the service group using a GET
    - self: Link to the current service group
    - upload: Link to upload files to the service group using a POST
    """

    available_files: List[FileMetadata]
    """The list of files returned by the query"""

    total_count: int
    """The total number of files that match the query regardless of skip and take values"""
