from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class MessageTemplateFields(JsonModel):
    """Fields representing the subject and body templates of a message."""

    subject_template: str
    """Subject template of the message."""

    body_template: str | None = None
    """Body template of the message."""


class MessageTemplate(JsonModel):
    """Model defining the notification content structure."""

    id: str | None = None
    """Gets or sets the ID for message template."""

    interpreting_service_name: str | None = None
    """Gets or sets the name of the interpreting service.

    Example: "smtp"
    """

    display_name: str | None = None
    """Gets or sets the message template's display name.

    Example: "name"
    """

    properties: Dict[str, str] | None = None
    """Gets or sets the message template's properties.

    Example: { "property": "value" }
    """

    fields: MessageTemplateFields
    """Gets or sets the message template's fields.

    Valid fields:
        - subjectTemplate (required)
        - bodyTemplate

    Example: { subjectTemplate: "subject", bodyTemplate: "body" }
    """

    referencing_notification_strategies: List[str] | None = None
    """Gets or sets the message template's referencing notification strategies."""
