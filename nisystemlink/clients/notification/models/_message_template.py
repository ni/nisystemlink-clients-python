from enum import Enum
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class MessageFieldTemplates(str, Enum):
    """Defines valid fields for message template."""
    subjectTemplate = "subjectTemplate"
    bodyTemplate = "bodyTemplate"


class MessageTemplate(JsonModel):
    """Model for message template defining notification content structure."""

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

    fields: Dict[MessageFieldTemplates, str]
    """Gets or sets the message template's fields.

    Valid fields:
        - subjectTemplate (required)
        - bodyTemplate

    Example: { MessageFieldTemplates.subjectTemplate: "subject", MessageFieldTemplates.bodyTemplate: "body" }
    """

    referencing_notification_strategies: List[str]
    """Gets or sets the message template's referencing notification strategies."""

    model_config = {"use_enum_values": True}
