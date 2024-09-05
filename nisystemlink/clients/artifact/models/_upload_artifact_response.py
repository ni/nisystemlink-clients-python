from nisystemlink.clients.core._uplink._json_model import JsonModel


class UploadArtifactResponse(JsonModel):
    """Response for an artifact upload request."""

    id: str
    """Information about the uploaded artifact."""
