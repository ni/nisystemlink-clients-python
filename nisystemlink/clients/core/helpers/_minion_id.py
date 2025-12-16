# -*- coding: utf-8 -*-

"""Helper function to get minion ID from Salt configuration."""

from nisystemlink.clients.core._internal._path_constants import PathConstants


def read_minion_id() -> str | None:
    """Read the minion ID from the Salt configuration.

    Returns:
        str | None: The minion ID content if the file exists, None otherwise.
    """
    minion_id_path = PathConstants.salt_data_directory / "conf" / "minion_id"

    if not minion_id_path.exists():
        return None

    try:
        with open(minion_id_path, "r", encoding="utf-8") as fp:
            return fp.read().strip()
    except (OSError, PermissionError):
        return None
