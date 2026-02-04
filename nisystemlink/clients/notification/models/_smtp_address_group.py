from typing import List, Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.notification.models._base_notification_metadata import (
    BaseNotificationMetadata,
)
from pydantic import model_validator


class SmtpAddressFields(JsonModel):
    """Recipient address fields used in SMTP messaging."""

    to_addresses: List[str] | None = None
    """List of primary recipient addresses."""

    cc_addresses: List[str] | None = None
    """List of carbon copy recipient addresses."""

    bcc_addresses: List[str] | None = None
    """List of blind carbon copy recipient addresses."""


class SmtpAddressGroup(BaseNotificationMetadata):
    """Model defining notification recipients for SMTP service."""

    interpreting_service_name: Literal["smtp"] = "smtp"
    """Service name for SMTP-based interpretation."""

    fields: SmtpAddressFields
    """Recipient address fields used for SMTP notifications.

    Valid fields:
        - to_addresses
        - cc_addresses
        - bcc_addresses

    Example:
        {
            to_addresses: [ "address1@example.com" ],
            cc_addresses: [ "address2@example.com" ],
            bcc_addresses: [ "address3@example.com" ]
        }
    """

    @model_validator(mode="before")
    @classmethod
    def set_interpreting_service_name(
        cls, data: "SmtpAddressGroup"
    ) -> "SmtpAddressGroup":
        if isinstance(data, dict) and "interpreting_service_name" not in data:
            data["interpreting_service_name"] = "smtp"
        return data
