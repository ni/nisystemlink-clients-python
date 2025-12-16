import uuid
from datetime import datetime

from nisystemlink.clients.alarm import AlarmClient
from nisystemlink.clients.alarm.models import (
    AlarmOrderBy,
    AlarmSeverityLevel,
    ClearAlarmTransition,
    CreateOrUpdateAlarmRequest,
    QueryAlarmsWithFilterRequest,
    SetAlarmTransition,
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
# alarm_id is a user-defined identifier for this alarm
alarm_id = f"example_alarm_{uuid.uuid1().hex}"

# Create an alarm with a SET transition
create_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=SetAlarmTransition(
        occurred_at=datetime.now(),
        severity_level=AlarmSeverityLevel.HIGH,
        condition="Temperature exceeded threshold",
        message="Temperature sensor reading: 85°C",
    ),
)
# Returns instance_id - a server-generated unique identifier for this specific alarm occurrence
id = client.create_or_update_alarm(create_request)

# Get the alarm by its instance ID (the unique occurrence identifier)
alarm = client.get_alarm(id)
print(f"Retrieved alarm: {alarm.alarm_id}, Condition: {alarm.condition}")

# Update the alarm with a higher severity (same alarm_id, updates the same instance)
update_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=SetAlarmTransition(
        occurred_at=datetime.now(),
        severity_level=AlarmSeverityLevel.CRITICAL,
        condition="Temperature critically high",
        message="Temperature sensor reading: 95°C",
    ),
)
client.create_or_update_alarm(update_request)

# Query alarms with a filter (can filter by alarm_id to find all instances)
# Include all transitions to see the full alarm history
query_request = QueryAlarmsWithFilterRequest(
    filter="alarmId=@0",
    substitutions=[alarm_id],
    order_by=AlarmOrderBy.UPDATED_AT,
    order_by_descending=True,
    transition_inclusion_option=TransitionInclusionOption.ALL,
    return_count=True,
)
query_response = client.query_alarms(query_request)

# Display query results
print(f"Total alarms found: {query_response.total_count}")
for alarm in query_response.alarms:
    print(f"  Alarm ID: {alarm.alarm_id}, Transitions: {len(alarm.transitions)}")
    for transition in alarm.transitions:
        print(f"    - {transition.transition_type}: {transition.condition}")

# Acknowledge the alarm
client.acknowledge_alarms(ids=[id])

# Clear the alarm
clear_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=ClearAlarmTransition(
        occurred_at=datetime.now(),
        condition="Temperature returned to normal",
    ),
)
client.create_or_update_alarm(clear_request)

# Delete the alarm by its instance ID
client.delete_alarm(id)
