"""Utilities for FileClient."""

from nisystemlink.clients.file import FileClient
from nisystemlink.clients.file.models import UpdateMetadataRequest


def rename_file(client: FileClient, file_id: str, name: str) -> None:
    """Rename a file identified by `file_id` to `name`.

    Args:
        client: The FileClient to use for the rename.
        file_id: ID of file to rename.
        name: New name for the File.
    """
    new_metadata = {"Name": name}
    rename_request = UpdateMetadataRequest(
        replace_existing=False, properties=new_metadata
    )
    client.update_metadata(metadata=rename_request, id=file_id)
