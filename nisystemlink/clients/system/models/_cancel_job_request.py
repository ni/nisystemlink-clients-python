from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class CancelJobRequest(JsonModel):
    """Model for cancel job request."""

    id: str = Field(alias="jid")
    """The ID of the job to cancel."""

    system_id: str
    """The system ID that the job to cancel targets."""
