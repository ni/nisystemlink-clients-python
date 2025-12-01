from datetime import datetime
from typing import Dict

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._link import Link


class BaseFileMetadata(JsonModel):
    """Base class for file metadata."""

    created: datetime | None = None
    """
    The date and time the file was created in the file service.

    example :2018-05-15T18:54:27.519Z
    """

    id: str | None = None
    """
    The file's ID within the service group.

    example: "5afb2ce3741fe11d88838cc9"
    """

    properties: Dict[str, str] | None = None
    """
    The file's properties
    Example - {"Name": "myfile.txt", "MyProperty": "Value"}
    """

    service_group: str | None = None
    """
    The service group that owns the file
    """

    size: int | None = None
    """
    The 32-bit file size in bytes. If the value is larger than a 32-bit integer,
    this value is -1 and the size64 parameter contains the correct value.
    """

    size64: int | None = None
    """
    The 64-bit file size in bytes
    """

    workspace: str | None = None
    """
    The workspace the file belongs to
    """


class FileMetadata(BaseFileMetadata):

    field_links: Dict[str, Link] | None = Field(None, alias="_links")
    """
    The links to access and manipulate the file:
    - data: Link to download the file using a GET request
    - delete: Link to delete the file using a DELETE request
    - self: Link to the file's metadata
    - updateMetadata: Link to update the file's metadata using a POST request
    """

    path: str | None = None
    """
    The path to the file on the server.  This field is returned only if
    the user has associated privileges to view file paths.

    example: C:\temp\4afb2ce3741fe11d88838cc9.txt
    """

    meta_data_revision: int | None = None
    """
    The file's properties revision number. When a file is uploaded, the revision number starts at 1.
    Every time metadata is updated, the revision number is incremented by 1.
    """

    last_updated_timestamp: datetime | None = None
    """
    The date and time the file was last updated in the file service.

    example: 2018-05-15T18:54:27.519Z
    """


class LinqQueryFileMetadata(BaseFileMetadata):
    """Metadata for a file returned by a LINQ query."""

    updated: datetime | None = None
    """
    The date and time the file was last updated in the file service.

    example :2018-05-15T18:54:27.519Z
    """
