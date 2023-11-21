from nisystemlink.clients.core._uplink._json_model import JsonModel


class UploadedFileInfo(JsonModel):
    """Uploaded file information"""

    uri: str
    """URI of the uploaded file"""
