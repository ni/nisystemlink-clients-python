import uuid
from datetime import datetime, timezone

from nisystemlink.clients.alarm import AlarmClient
from nisystemlink.clients.alarm.models import (
    AcknowledgeByInstanceIdRequest,
    CreateOrUpdateAlarmRequest,
    DeleteByInstanceIdRequest,
    QueryWithFilterRequest,
)
from nisystemlink.clients.alarm.models._alarm import AlarmTransitionType
from nisystemlink.clients.alarm.models._create_or_update_alarm_request import (
    CreateAlarmTransition,
)
from nisystemlink.clients.alarm.models._query_alarms_request import (
    AlarmOrderBy,
    TransitionInclusionOption,
)
from nisystemlink.clients.core import HttpConfiguration

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = AlarmClient(configuration=server_configuration)

# Create a unique alarm ID for this example
alarm_id = f"example_alarm_{uuid.uuid1().hex}"

# Create an alarm with a SET transition
create_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=CreateAlarmTransition(
        transition_type=AlarmTransitionType.SET,
        occurred_at=datetime.now(timezone.utc),
        severity_level=3,
        condition="Temperature exceeded threshold",
        message="Temperature sensor reading: 85°C",
    ),
)
create_response = client.create_or_update_alarm(create_request)
instance_id = create_response.instance_id

# Get the alarm by instance ID
alarm = client.get_alarm(instance_id)

# Update the alarm with a higher severity
update_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=CreateAlarmTransition(
        transition_type=AlarmTransitionType.SET,
        occurred_at=datetime.now(timezone.utc),
        severity_level=5,
        condition="Temperature critically high",
        message="Temperature sensor reading: 95°C",
    ),
)
update_response = client.create_or_update_alarm(update_request)

# Query alarms with a filter
query_request = QueryWithFilterRequest(
    filter=f'alarmId="{alarm_id}"',
    transition_inclusion_option=TransitionInclusionOption.ALL,
    order_by=AlarmOrderBy.UPDATED_AT,
    order_by_descending=True,
    return_count=True,
)
query_response = client.query_alarms(query_request)

# Acknowledge the alarm
ack_request = AcknowledgeByInstanceIdRequest(instance_ids=[instance_id])
ack_response = client.acknowledge_instances_by_instance_id(ack_request)

# Clear the alarm
clear_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=CreateAlarmTransition(
        transition_type=AlarmTransitionType.CLEAR,
        occurred_at=datetime.now(timezone.utc),
        severity_level=0,
        condition="Temperature returned to normal",
    ),
)
clear_response = client.create_or_update_alarm(clear_request)

# Delete the alarm by instance ID
client.delete_alarm(instance_id)
