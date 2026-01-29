from typing import Dict

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dynamic_notification_strategy import DynamicNotificationStrategy


class DynamicStrategyRequest(JsonModel):
    """Request model for applying a dynamic notification strategy."""

    message_template_substitution_fields: Dict[str, str] | None = None
    """Defines the fields used for substituting values in the message template.

    Example: { "replacement": "value" }
    """

    notification_strategy: DynamicNotificationStrategy
    """Notification strategy containing configurations for address groups and message templates."""
