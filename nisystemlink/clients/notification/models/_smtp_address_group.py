from typing import List, Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.notification.models._address_group import AddressGroup


class SmtpAddressFields(JsonModel):
    """Fields representing the subject and body templates of a message."""

    toAddresses: List[str] | None = None
    """List of primary recipient addresses."""

    ccAddresses: List[str] | None = None
    """List of carbon copy recipient addresses."""

    bccAddresses: List[str] | None = None
    """List of blind carbon copy recipient addresses."""


class SmtpAddressGroup(AddressGroup):
    interpreting_service_name: Literal["smtp"]
    fields: SmtpAddressFields
