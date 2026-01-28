import uuid
from datetime import datetime

# from urllib.parse import urlsplit, urlunsplit

from nisystemlink.clients.alarm import AlarmClient
from nisystemlink.clients.alarm.models._alarm import Alarm, AlarmSeverityLevel
from nisystemlink.clients.alarm.models._create_or_update_alarm_request import (
    ClearAlarmTransition,
    CreateOrUpdateAlarmRequest,
    SetAlarmTransition,
)
from nisystemlink.clients.core import HttpConfiguration
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


# Create request for applying strategy
def create_notification_request_for_alarm(
    retrieved_alarm: Alarm,
    address_group: AddressGroup,
    message_template: MessageTemplate,
) -> DynamicStrategyRequest:
    """Creates and returns a dynamic strategy request."""
    occurred_at = retrieved_alarm.most_recent_transition_occurred_at

    return DynamicStrategyRequest(
        message_template_substitution_fields={
            "alarm_id": retrieved_alarm.alarm_id,
            "alarm_condition": retrieved_alarm.condition,
            "alarm_description": retrieved_alarm.description,
            "alarm_severity": str(retrieved_alarm.current_severity_level),
            "alarm_occurred_at": occurred_at.isoformat() if occurred_at else "",
        },
        notification_strategy=DynamicNotificationStrategy(
            notification_configurations=[
                DynamicNotificationConfiguration(
                    address_group=address_group,
                    message_template=message_template,
                )
            ]
        ),
    )


# Create clients for Notification and Alarm services
notification_client = NotificationClient(configuration=server_configuration)
alarm_client = AlarmClient(configuration=server_configuration)

# Create a unique alarm ID for this example
alarm_id = f"example_alarm_{uuid.uuid1().hex}"

# Create an alarm with a SET transition
create_alarm_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=SetAlarmTransition(
        occurred_at=datetime.now(),
        severity_level=AlarmSeverityLevel.HIGH,
        value="85",
        condition="Greater than 80",
        short_text="Temperature is high",
        detail_text="Temperature sensor reading is 85°C (higher than the configured threshold of 80°C)",
    ),
    description="Example alarm for notification",
)
id = alarm_client.create_or_update_alarm(create_alarm_request)
print("Alarm created successfully")

# Get the alarm by its instance ID (the unique occurrence identifier)
retrieved_alarm = alarm_client.get_alarm(instance_id=id)

# Define recipients to notify
recipients = AddressFields(toAddresses=["sample1@example.com"])

# Create address group
address_group = AddressGroup(
    interpreting_service_name="smtp",
    fields=recipients,
)

# Create mail template for alarm creation notification
alarm_creation_template = MessageTemplate(
    interpreting_service_name="smtp",
    display_name="Alarm Creation Template",
    fields=MessageTemplateFields(
        subject_template="Alarm Created: <alarm_id>",
        body_template="An alarm with ID <alarm_id> has been created.\n"
        "Condition: <alarm_condition>\n"
        "Description: <alarm_description>\n"
        "Current severity: <alarm_severity>\n"
        "Occurred At: <alarm_occurred_at>",
    ),
)

# Create mail template for alarm deletion notification
alarm_deletion_template = MessageTemplate(
    display_name="Alarm Deletion Template",
    fields=MessageTemplateFields(
        subject_template="Alarm Cleared: <alarm_id>",
        body_template="The alarm with ID <alarm_id> has been cleared.\n"
        "Condition: <alarm_condition>\n"
        "Description: <alarm_description>",
    ),
)


# Send notification for alarm creation
notification_for_alarm_creation = create_notification_request_for_alarm(
    retrieved_alarm=retrieved_alarm,
    address_group=address_group,
    message_template=alarm_creation_template,
)
notification_client.apply_notification_strategy(request=notification_for_alarm_creation)
print("Notification sent for alarm creation")

# Clear the alarm
clear_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=ClearAlarmTransition(
        occurred_at=datetime.now(),
        condition="Temperature returned to normal",
    ),
)

result = alarm_client.create_or_update_alarm(clear_request, ignore_conflict=True)
if result is None:
    print("No state change needed (alarm already in requested state)")
else:
    print("Alarm cleared successfully")

alarm_client.delete_alarm(instance_id=id)
print("Alarm deleted successfully")

# Send notification for alarm deletion
notification_for_alarm_deletion = create_notification_request_for_alarm(
    retrieved_alarm=retrieved_alarm,
    address_group=address_group,
    message_template=alarm_deletion_template,
)

notification_client.apply_notification_strategy(request=notification_for_alarm_deletion)
print("Notification sent for alarm deletion")
