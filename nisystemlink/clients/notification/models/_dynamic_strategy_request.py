from typing import Dict

from ._notification_strategy import NotificationStrategy

from nisystemlink.clients.core._uplink._json_model import JsonModel


class DynamicStrategyRequest(JsonModel):
    """Request model for applying a notification strategy."""

    message_template_substitution_fields: Dict[str, str]
    """Gets or sets the message template substitution fields.

    Example: { "replacement": "value" }
    """

    notification_strategy: NotificationStrategy
    """Gets or sets the notification strategy containing configurations for address groups and message templates."""
