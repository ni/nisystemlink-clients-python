from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dynamic_notification_configuration import DynamicNotificationConfiguration


class DynamicNotificationStrategy(JsonModel):
    """Model for the notification strategy to be applied."""

    notification_configurations: List[DynamicNotificationConfiguration]
    """Gets the notification configurations associated with this strategy."""
