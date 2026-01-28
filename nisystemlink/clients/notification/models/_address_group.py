from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._common_meta_data import BaseNotificationMetadata


class AddressFields(JsonModel):
    """Fields representing the subject and body templates of a message."""

    toAddresses: List[str] | None = None
    """List of primary recipient addresses."""

    ccAddresses: List[str] | None = None
    """List of carbon copy recipient addresses."""

    bccAddresses: List[str] | None = None
    """List of blind carbon copy recipient addresses."""


class AddressGroup(BaseNotificationMetadata):
    """Model defining notification recipients."""

    interpreting_service_name: str
    """Gets or sets the name of the interpreting service.

    Example: "smtp"
    """

    fields: AddressFields
    """Gets or sets the address group's fields. Requires at least one valid recipient.

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
