from datetime import datetime

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import AliasChoices, Field


class UploadSessionStartResponse(JsonModel):
    """Response model for starting an upload session."""

    session_id: str = Field(
        validation_alias=AliasChoices("session_id", "id"),
        serialization_alias="id",
    )
    """
    The id created for the upload session.
    """

    created_at: datetime
    """
    The date and time the upload session has started.
    """
