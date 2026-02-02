from typing import Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.notification.models._base_notification_metadata import (
    BaseNotificationMetadata,
)
from pydantic import model_validator


class SmtpMessageTemplateFields(JsonModel):
    """Template fields to construct an SMTP message."""

    subject_template: str
    """Subject template of the message."""

    body_template: str | None = None
    """Body template of the message."""


class SmtpMessageTemplate(BaseNotificationMetadata):
    """Model defining message template for SMTP service"""

    interpreting_service_name: Literal["smtp"] = "smtp"
    """Service name for SMTP-based interpretation."""

    fields: SmtpMessageTemplateFields
    """Subject and body template fields for SMTP messages."""

    @model_validator(mode="before")
    @classmethod
    def set_interpreting_service_name(
        cls, data: "SmtpMessageTemplate"
    ) -> "SmtpMessageTemplate":
        if isinstance(data, dict) and "interpreting_service_name" not in data:
            data["interpreting_service_name"] = "smtp"
        return data
