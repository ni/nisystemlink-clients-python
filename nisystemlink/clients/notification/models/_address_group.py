from typing import Dict, List

from ._base_notification_metadata import BaseNotificationMetadata


class AddressGroup(BaseNotificationMetadata):
    """Model defining notification recipients for generic service."""

    interpreting_service_name: str
    """Name of the interpreting service."""

    fields: Dict[str, List[str]]
    """Address group's fields. Requires at least one valid recipient."""
