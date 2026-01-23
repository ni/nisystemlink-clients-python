from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AddressFields(JsonModel):
    """Fields representing the subject and body templates of a message."""

    toAddresses: List[str] | None = None
    """List of primary recipient addresses."""

    ccAddresses: List[str] | None = None
    """List of carbon copy recipient addresses."""

    bccAddresses: List[str] | None = None
    """List of blind carbon copy recipient addresses."""


class AddressGroup(JsonModel):
    """Model defining notification recipients."""

    id: str | None = None
    """Gets or sets the ID for address group."""

    interpreting_service_name: str
    """Gets or sets the name of the interpreting service.

    Example: "smtp"
    """

    display_name: str | None = None
    """Gets or sets the address group's display name.

    Example: "name"
    """

    properties: Dict[str, str] | None = None
    """Gets or sets the address group's properties.

    Example: { "property": "value" }
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

    referencing_notification_strategies: List[str] | None = None
    """Gets or sets the address group's referencing notification strategies."""
