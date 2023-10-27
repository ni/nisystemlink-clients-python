from __future__ import annotations

from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._webapp_models import Error, WebApp


class WebAppsResponse(JsonModel):
    webapps: Optional[List[WebApp]]
    """
    List of webapps.
    """
    continuation_token: Optional[str] = Field(
        None, alias="continuationToken", example="token"
    )
    """
    The continuation token can be used to paginate through the webapp query results. Provide this token in the next query webapps call.
    """
    error: Optional[Error]
    """
    Error response.
    """
