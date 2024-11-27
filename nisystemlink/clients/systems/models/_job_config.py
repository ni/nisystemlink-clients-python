from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class JobConfig(JsonModel):
    """The configuration of the job."""

    user: Optional[str] = None
    """The user who created the job."""

    tgt: Optional[List[str]] = None
    """The target systems for the job."""

    fun: Optional[List[str]] = None
    """Salt functions related to the job."""

    arg: Optional[List[str]] = None
    """Arguments of the salt functions."""
