from nisystemlink.clients.core._api_exception import ApiException
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.notification.models._smtp_address_group import (
    SmtpAddressGroup,
)
from nisystemlink.clients.notification.models._smtp_message_template import (
    SmtpMessageTemplate,
)
from pydantic import Field, model_validator


from ._address_group import AddressGroup
from ._message_template import MessageTemplate


class DynamicNotificationConfiguration(JsonModel):
    """Model for notification configuration defining address groups and message template for the notification.

    Requires at least one of addressGroupId or addressGroup, and one of messageTemplateId or messageTemplate.
    """

    address_group_id: str | None = None
    """ID referencing the associated address group."""

    message_template_id: str | None = None
    """ID referencing the associated message template."""

    address_group: SmtpAddressGroup | AddressGroup | None = Field(
        default=None, discriminator="interpreting_service_name"
    )
    """Gets the address group defining notification recipients."""

    message_template: SmtpMessageTemplate | MessageTemplate | None = Field(
        default=None, discriminator="interpreting_service_name"
    )
    """Gets the message template defining notification content structure"""

    @model_validator(mode="after")
    def validate_required_pairs(self):
        if self.address_group_id is None and self.address_group is None:
            raise ApiException("AddressGroupId is required.")

        if self.message_template_id is None and self.message_template is None:
            raise ApiException("MessageTemplateId is required.")

        return self
