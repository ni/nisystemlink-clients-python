from typing import Any, Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class CreateJobRequest(JsonModel):
    """Model for create job request."""

    arg: Optional[List[List[str]]] = None
    """List of arguments to the functions specified in the "fun" property."""

    tgt: Optional[List[str]] = None
    """List of system IDs on which to run the job."""

    fun: Optional[List[str]] = None
    """Functions contained in the job."""

    metadata: Optional[Dict[str, Any]] = None
    """Additional information of the job."""
