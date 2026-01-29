from typing import Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.notification.models._message_template import \
    MessageTemplate


class SmtpMessageTemplateFields(JsonModel):
    """Fields representing the subject and body templates of a message."""

    subject_template: str
    """Subject template of the message."""

    body_template: str | None = None
    """Body template of the message."""


class SmtpMessageTemplate(MessageTemplate):
    interpreting_service_name: Literal["smtp"]
    fields: SmtpMessageTemplateFields
