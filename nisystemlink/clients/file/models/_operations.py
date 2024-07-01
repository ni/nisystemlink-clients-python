from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class Operation5(JsonModel):
    available: bool
    """
    Whether the operation is available to the caller
    """
    version: Optional[int] = None
    """
    The version of the available operation
    """


class Operations(JsonModel):
    delete_files: Optional[Operation5] = Field(None, alias="deleteFiles")
    download_data: Optional[Operation5] = Field(None, alias="downloadData")
    list_files: Optional[Operation5] = Field(None, alias="listFiles")
    query_files: Optional[Operation5] = Field(None, alias="queryFiles")
    update_metadata: Optional[Operation5] = Field(None, alias="updateMetadata")
    upload_files: Optional[Operation5] = Field(None, alias="uploadFiles")


class V1Operations(JsonModel):
    operations: Optional[Operations] = None
    """
    Available operations in the v1 version of the API:
    - deleteFiles: The ability to delete uploaded files
    - downloadData: The ability to download file data
    - listFiles: The ability to list available files and service groups
    - queryFiles: The ability to query available files and service groups
    - updateMetadata: The ability to update file metadata properties
    - uploadFiles: The ability to upload files
    """
