from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class MessageTemplate(JsonModel):
    """Model for message template for v1 endpoint."""

    id: str
    """Gets or sets the ID for message template."""

    interpreting_service_name: str
    """Gets or sets the name of the interpreting service.

    Example: "smtp"
    """

    display_name: str
    """Gets or sets the message template's display name.

    Example: "name"
    """

    properties: Dict[str, str]
    """Gets or sets the message template's properties.

    Example: { "property": "value" }
    """

    fields: Dict[str, str]
    """Gets or sets the message template's fields.

    Valid fields:
        - subjectTemplate (required)
        - bodyTemplate

    Example: { "subjectTemplate": "subject", "bodyTemplate": "body" }
    """

    referencing_notification_strategies: List[str]
    """Gets or sets the message template's referencing notification strategies."""
