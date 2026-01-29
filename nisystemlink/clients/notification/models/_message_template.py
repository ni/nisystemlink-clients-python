from typing import Dict

from ._base_notification_metadata import BaseNotificationMetadata


class MessageTemplate(BaseNotificationMetadata):
    """Model defining the notification content structure."""

    interpreting_service_name: str
    """Service identifier for generic interpretation."""

    fields: Dict[str, str]
    """Template fields for message."""
