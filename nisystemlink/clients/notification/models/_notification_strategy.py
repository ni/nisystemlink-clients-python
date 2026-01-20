from typing import List
from ._notification_configuration import NotificationConfiguration
from nisystemlink.clients.core._uplink._json_model import JsonModel


class NotificationStrategy(JsonModel):
    """Model for the notification strategy to be applied."""

    notification_configurations: List[NotificationConfiguration]
    """Gets the notification configurations associated with this strategy."""
