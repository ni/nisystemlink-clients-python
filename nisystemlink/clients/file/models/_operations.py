from typing import Optional

from nisystemlink.clients.core._api_info import Operation
from nisystemlink.clients.core._uplink._json_model import JsonModel


class Operations(JsonModel):
    delete_files: Optional[Operation]
    download_data: Optional[Operation]
    list_files: Optional[Operation]
    query_files: Optional[Operation]
    update_metadata: Optional[Operation]
    upload_files: Optional[Operation]


class V1Operations(JsonModel):
    operations: Optional[Operations]
    """
    Available operations in the v1 version of the API:
    - deleteFiles: The ability to delete uploaded files
    - downloadData: The ability to download file data
    - listFiles: The ability to list available files and service groups
    - queryFiles: The ability to query available files and service groups
    - updateMetadata: The ability to update file metadata properties
    - uploadFiles: The ability to upload files
    """
