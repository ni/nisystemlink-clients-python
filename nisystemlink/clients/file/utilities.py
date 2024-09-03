"""Utilities for FileClient."""

from nisystemlink.clients.file import FileClient
from nisystemlink.clients.file.models import UpdateMetadataRequest


def get_file_id_from_uri(uri: str) -> str:
    """Get the File ID from a file URI.

    Example: URI "/nifile/v1/service-groups/Default/files/5b874c4adedd0f1c78a22a96" returns "5b874c4adedd0f1c78a22a96"

    Args:
        uri: URI of a file on SystemLink

    Returns:
        ID of the File extracted from the `uri`.
    """
    # Split the uri by '/' and get the last part
    parts = uri.split("/")
    return parts[-1]


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
    client.update_metadata(metadata=rename_request, file_id=file_id)
