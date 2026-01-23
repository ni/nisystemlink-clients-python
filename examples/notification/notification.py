import uuid

from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.notification import NotificationClient
from nisystemlink.clients.notification.models import (
    AddressFields,
    AddressGroup,
    DynamicNotificationConfiguration,
    DynamicNotificationStrategy,
    DynamicStrategyRequest,
    MessageTemplate,
    MessageTemplateFields,
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = NotificationClient(configuration=server_configuration)

# Create a unique address group ID for this example
address_group_id = uuid.uuid1().hex

# Create a unique message template ID for this example
message_template_id = uuid.uuid1().hex

# Create address group
address_group = AddressGroup(
    id=address_group_id,
    interpreting_service_name="smtp",
    display_name="Address group name",
    properties={"property": "value"},
    fields=AddressFields(
        toAddresses=["sample1@example.com"],
        ccAddresses=["sample2@example.com"],
        bccAddresses=["sample3@example.com"],
    ),
    referencing_notification_strategies=["reference_notification_strategy"],
)

# Create message template
message_template = MessageTemplate(
    id=message_template_id,
    interpreting_service_name="smtp",
    display_name="Message template name",
    properties={"property": "value"},
    fields=MessageTemplateFields(
        subject_template="Sample Subject", body_template="Sample Body"
    ),
    referencing_notification_strategies=["reference_notification_strategy"],
)

# Create notification configuration
dynamic_notification_config = DynamicNotificationConfiguration(
    address_group_id=address_group_id,
    message_template_id=message_template_id,
    address_group=address_group,
    message_template=message_template,
)

# Create notification strategy
dynamic_notification_strategy = DynamicNotificationStrategy(
    notification_configurations=[dynamic_notification_config]
)

# Create request for applying strategy
dynamic_strategy_request = DynamicStrategyRequest(
    message_template_substitution_fields={"replacement": "value"},
    notification_strategy=dynamic_notification_strategy,
)

try:
    client.apply_notification_strategy(request=dynamic_strategy_request)
    print("Notification strategy applied successfully")
except ApiException as e:
    if e.http_status_code == 400:
        print("Bad request body")
    elif e.http_status_code == 401:
        print("Unauthorized access")
    else:
        raise
