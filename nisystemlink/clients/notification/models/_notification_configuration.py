from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._address_group import AddressGroup
from ._message_template import MessageTemplate


class NotificationConfiguration(JsonModel):
    """Model for notification configuration defining address groups and message template for the notification."""

    address_group_id: str
    """Gets the address group ID"""

    message_template_id: str
    """Gets the message template ID"""

    address_group: AddressGroup
    """Gets the address group defining notification recipients."""

    message_template: MessageTemplate
    """Gets the message template defining notification content structure"""
