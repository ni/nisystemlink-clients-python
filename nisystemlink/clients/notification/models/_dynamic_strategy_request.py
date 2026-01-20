from typing import Dict

from ._notification_strategy import NotificationStrategy

from nisystemlink.clients.core._uplink._json_model import JsonModel


class DynamicStrategyRequest(JsonModel):
    """Model for an object describing the properties of the strategy to be applied."""

    message_template_substitution_fields: Dict[str, str]
    """Gets or sets the message template substitution fields.

    Example: { "replacement": "value" }
    """

    notification_strategy: NotificationStrategy
    """This record defines the dynamic notification strategy model for the v1 endpoint."""
