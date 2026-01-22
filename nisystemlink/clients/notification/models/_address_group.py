from enum import Enum
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AddressFields(str, Enum):
    """Defines valid fields for address group."""
    toAddresses = "toAddresses"
    ccAddresses = "ccAddresses"
    bccAddresses = "bccAddresses"


class AddressGroup(JsonModel):
    """Model for address group defining notification recipients."""

    id: str
    """Gets or sets the ID for address group."""

    interpreting_service_name: str
    """Gets or sets the name of the interpreting service.

    Example: "smtp"
    """

    display_name: str
    """Gets or sets the address group's display name.

    Example: "name"
    """

    properties: Dict[str, str]
    """Gets or sets the address group's properties.

    Example: { "property": "value" }
    """

    fields: Dict[AddressFields, List[str]]
    """Gets or sets the address group's fields. Requires at least one valid recipient.

    Valid fields:
        - toAddresses
        - ccAddresses
        - bccAddresses

    Example:
        {
            AddressFields.toAddresses: [ "address1@example.com" ],
            AddressFields.ccAddresses: [ "address2@example.com" ],
            AddressFields.bccAddresses: [ "address3@example.com" ]
        }
    """

    referencing_notification_strategies: List[str]
    """Gets or sets the address group's referencing notification strategies."""

    model_config = {"use_enum_values": True}
