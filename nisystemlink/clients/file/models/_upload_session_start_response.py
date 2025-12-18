from datetime import datetime

from nisystemlink.clients.core._uplink._json_model import JsonModel


class UploadSessionStartResponse(JsonModel):
    """Response model for starting an upload session."""

    id: str
    """
    The session id created.
    
    example: 54837669-8cf5-469e-bf7d-26cb808c8f24
    """

    created_at: datetime
    """
    The date and time the upload session has started.
    
    example: 2018-05-15T18:54:27.519Z
    """
