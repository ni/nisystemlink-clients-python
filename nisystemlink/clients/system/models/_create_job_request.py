from typing import Any, Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class CreateJobRequest(JsonModel):
    """Model for create job request."""

    arg: Optional[List[List[str]]] = None
    """Arguments of the salt functions."""

    tgt: Optional[List[str]] = None
    """The target systems for the job."""

    fun: Optional[List[str]] = None
    """Salt functions related to the job."""

    metadata: Optional[Dict[str, Any]] = None
    """The metadata associated with the job."""
