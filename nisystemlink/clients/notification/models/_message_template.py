from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._common_meta_data import CommonFields


class MessageTemplateFields(JsonModel):
    """Fields representing the subject and body templates of a message."""

    subject_template: str
    """Subject template of the message."""

    body_template: str | None = None
    """Body template of the message."""


class MessageTemplate(CommonFields):
    """Model defining the notification content structure."""

    fields: MessageTemplateFields
    """Gets or sets the message template's fields.

    Valid fields:
        - subjectTemplate (required)
        - bodyTemplate

    Example: { subjectTemplate: "subject", bodyTemplate: "body" }
    """
