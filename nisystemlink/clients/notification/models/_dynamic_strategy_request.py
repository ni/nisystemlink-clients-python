from typing import Dict

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dynamic_notification_strategy import DynamicNotificationStrategy


class DynamicStrategyRequest(JsonModel):
    """Request model for applying a dynamic notification strategy."""

    message_template_substitution_fields: Dict[str, str] | None = None
    """Gets or sets the message template substitution fields.

    Example: { "replacement": "value" }
    """

    notification_strategy: DynamicNotificationStrategy
    """Gets or sets the notification strategy containing configurations for address groups and message templates."""
