from nisystemlink.clients.core._api_info import Operation
from nisystemlink.clients.core._uplink._json_model import JsonModel


class V1Operations(JsonModel):
    """The operations available in the routes provided by the v2 HTTP API."""

    upload_artifacts: Operation
    """The ability to upload artifacts."""

    download_artifacts: Operation
    """The ability to download artifacts."""