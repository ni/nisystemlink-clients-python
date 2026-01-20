from ._address_group import AddressGroup
from ._message_template import MessageTemplate

from nisystemlink.clients.core._uplink._json_model import JsonModel


class NotificationConfiguration(JsonModel):
    """Model for dynamic notification configuration for the v1 endpoint."""

    address_group_id: str
    """Gets the address group ID"""

    message_template_id: str
    """Gets the message template ID"""

    address_group: AddressGroup
    """This record defines the address group model for the v1 endpoint."""

    message_template: MessageTemplate
    """This record defines the message template model for the v1 endpoint."""
