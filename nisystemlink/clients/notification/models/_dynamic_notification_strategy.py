from typing import Annotated, List


from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._dynamic_notification_configuration import DynamicNotificationConfiguration


class DynamicNotificationStrategy(JsonModel):
    """Model for the notification strategy to be applied."""

    notification_configurations: Annotated[
        List[DynamicNotificationConfiguration], Field(min_length=1)
    ]
    """Notification configurations associated with this strategy."""
