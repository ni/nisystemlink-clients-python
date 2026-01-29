from typing import List, Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.notification.models._base_notification_metadata import (
    BaseNotificationMetadata,
)


class SmtpAddressFields(JsonModel):
    """Recipient address fields used in SMTP messaging."""

    toAddresses: List[str] | None = None
    """List of primary recipient addresses."""

    ccAddresses: List[str] | None = None
    """List of carbon copy recipient addresses."""

    bccAddresses: List[str] | None = None
    """List of blind carbon copy recipient addresses."""


class SmtpAddressGroup(BaseNotificationMetadata):
    """Model defining notification recipients for SMTP service."""

    interpreting_service_name: Literal["smtp"]
    """Service name for SMTP-based interpretation."""

    fields: SmtpAddressFields
    """Recipient address fields used for SMTP notifications.

    Valid fields:
        - toAddresses
        - ccAddresses
        - bccAddresses

    Example:
        {
            toAddresses: [ "address1@example.com" ],
            ccAddresses: [ "address2@example.com" ],
            bccAddresses: [ "address3@example.com" ]
        }
    """
