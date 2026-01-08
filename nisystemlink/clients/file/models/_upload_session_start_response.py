from datetime import datetime

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class UploadSessionStartResponse(JsonModel):
    """Response model for starting an upload session."""

    session_id: str = Field(alias="id")
    """
    The id created for the upload session.
    """

    created_at: datetime
    """
    The date and time the upload session has started.
    """
