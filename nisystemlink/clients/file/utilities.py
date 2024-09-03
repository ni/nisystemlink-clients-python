"""Utilities for FileClient."""


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
