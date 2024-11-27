from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class CancelJobRequest(JsonModel):
    """Cancel job modal."""

    jid: Optional[str] = None
    """The ID of the job to cancel."""

    system_id: Optional[str] = None
    """The system ID that the job to cancel targets."""
