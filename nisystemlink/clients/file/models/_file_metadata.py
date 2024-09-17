from datetime import datetime
from typing import Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._link import Link


class FileMetadata(JsonModel):
    field_links: Optional[Dict[str, Link]] = Field(None, alias="_links")
    """
    The links to access and manipulate the file:
    - data: Link to download the file using a GET request
    - delete: Link to delete the file using a DELETE request
    - self: Link to the file's metadata
    - updateMetadata: Link to update the file's metadata using a POST request
    """

    created: Optional[datetime]
    """
    The date and time the file was created in the file service.

    example :2018-05-15T18:54:27.519Z
    """

    id: Optional[str]
    """
    The file's ID within the service group.

    example: "5afb2ce3741fe11d88838cc9"
    """

    path: Optional[str]
    """
    The path to the file on the server.  This field is returned only if
    the user has associated privileges to view file paths.

    example: C:\temp\4afb2ce3741fe11d88838cc9.txt
    """

    properties: Optional[Dict[str, str]]
    """
    The file's properties
    Example - {"Name": "myfile.txt", "MyProperty": "Value"}
    """

    meta_data_revision: Optional[int]
    """
    The file's properties revision number. When a file is uploaded, the revision number starts at 1.
    Every time metadata is updated, the revision number is incremented by 1.
    """

    service_group: Optional[str]
    """
    The service group that owns the file
    """

    size: Optional[int]
    """
    The 32-bit file size in bytes. If the value is larger than a 32-bit integer,
    this value is -1 and the size64 parameter contains the correct value.
    """

    size64: Optional[int]
    """
    The 64-bit file size in bytes
    """

    workspace: Optional[str]
    """
    The workspace the file belongs to
    """

    last_updated_timestamp: Optional[datetime]
    """
    The date and time the file was last updated in the file service.

    example: 2018-05-15T18:54:27.519Z
    """
