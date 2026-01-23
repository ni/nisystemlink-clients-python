from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._address_group import AddressGroup
from ._message_template import MessageTemplate


class DynamicNotificationConfiguration(JsonModel):
    """Model for notification configuration defining address groups and message template for the notification."""

    address_group_id: str | None = None
    """Gets the address group ID"""

    message_template_id: str | None = None
    """Gets the message template ID"""

    address_group: AddressGroup | None = None
    """Gets the address group defining notification recipients."""

    message_template: MessageTemplate | None = None
    """Gets the message template defining notification content structure"""
