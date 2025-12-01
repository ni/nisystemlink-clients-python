from nisystemlink.clients.core._api_info import Operation
from nisystemlink.clients.core._uplink._json_model import JsonModel


class Operations(JsonModel):
    delete_files: Operation | None = None
    download_data: Operation | None = None
    list_files: Operation | None = None
    query_files: Operation | None = None
    update_metadata: Operation | None = None
    upload_files: Operation | None = None


class V1Operations(JsonModel):
    operations: Operations | None = None
    """
    Available operations in the v1 version of the API:
    - deleteFiles: The ability to delete uploaded files
    - downloadData: The ability to download file data
    - listFiles: The ability to list available files and service groups
    - queryFiles: The ability to query available files and service groups
    - updateMetadata: The ability to update file metadata properties
    - uploadFiles: The ability to upload files
    """
