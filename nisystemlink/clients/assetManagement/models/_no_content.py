from typing import Optional
from nisystemlink.clients.core._uplink._json_model import JsonModel


class NoContentResult(JsonModel):

    status_code: Optional[int] = None