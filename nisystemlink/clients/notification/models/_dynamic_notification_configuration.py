from __future__ import annotations

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.notification.models._address_group import AddressGroup
from nisystemlink.clients.notification.models._message_template import MessageTemplate
from nisystemlink.clients.notification.models._smtp_address_group import (
    SmtpAddressGroup,
)
from nisystemlink.clients.notification.models._smtp_message_template import (
    SmtpMessageTemplate,
)
from pydantic import Field, model_validator


class DynamicNotificationConfiguration(JsonModel):
    """Model for notification configuration defining address groups and message template for the notification.

    Requires at least one of addressGroupId or addressGroup, and one of messageTemplateId or messageTemplate.
    """

    address_group_id: str | None = None
    """ID referencing the associated address group."""

    message_template_id: str | None = None
    """ID referencing the associated message template."""

    address_group: AddressGroup | SmtpAddressGroup | None = Field(default=None)
    """Address group defining notification recipients."""

    message_template: MessageTemplate | SmtpMessageTemplate | None = Field(default=None)
    """Message template defining notification content structure"""

    @model_validator(mode="after")
    def validate_required_pairs(self) -> DynamicNotificationConfiguration:
        """Validator to check at least one of address_group_id or address_group, and
        one of message_template_id or message_template is present.
        """
        if self.address_group_id is None and self.address_group is None:
            raise ValueError(
                "One of either AddressGroupId or AddressGroup is required."
            )

        if self.message_template_id is None and self.message_template is None:
            raise ValueError(
                "One of either MessageTemplateId or MessageTemplate is required."
            )

        return self
