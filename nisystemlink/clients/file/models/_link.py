from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class Link(JsonModel):
    href: str = Field(..., example="/nifile/v1/service-groups")
    """
    URI of the link
    """
