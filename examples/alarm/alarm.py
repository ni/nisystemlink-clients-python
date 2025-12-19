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
from nisystemlink.clients.core import ApiException, HttpConfiguration

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
        value="85",
        condition="Greater than 80",
        short_text="Temperature is high",
        detail_text="Temperature sensor reading is 85°C (higher than the configured threshold of 80°C)",
    ),
)
# Returns instance_id - a server-generated unique identifier for this specific alarm occurrence
id = client.create_or_update_alarm(create_request)

# Get the alarm by its instance ID (the unique occurrence identifier)
alarm = client.get_alarm(instance_id=id)
print(f"Retrieved alarm: {alarm.alarm_id}, Condition: {alarm.condition}")

# Update the alarm with a higher severity (same alarm_id, updates the same instance)
update_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=SetAlarmTransition(
        occurred_at=datetime.now(),
        severity_level=AlarmSeverityLevel.CRITICAL,
        value="95",
        condition="Greater than 90",
        short_text="Temperature is critical",
        detail_text="Temperature sensor reading is 95°C (higher than the configured threshold of 90°C)",
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
        print(f"- {transition.transition_type}: {transition.condition}")

# Acknowledge the alarm
client.acknowledge_alarms(instance_ids=[id])

# Clear the alarm with 409 conflict handling - Method 1: Manual exception handling
# A 409 Conflict response indicates that the requested transition would not change the alarm's state.
# This allows stateless applications to simply attempt state transitions without first checking
# the current state. For example, a monitoring system can repeatedly try to CLEAR an alarm
# when conditions return to normal, and the API will return 409 if already cleared.
clear_request = CreateOrUpdateAlarmRequest(
    alarm_id=alarm_id,
    transition=ClearAlarmTransition(
        occurred_at=datetime.now(),
        condition="Temperature returned to normal",
    ),
)
try:
    client.create_or_update_alarm(clear_request)
    print("Alarm cleared successfully")
except ApiException as e:
    if e.http_status_code == 409:
        print("Alarm is already in the requested state (409 Conflict)")
    else:
        raise

# Clear the alarm with 409 conflict handling - Method 2: Using ignore_conflict parameter
# This approach is cleaner for stateless applications that don't care about 409 errors.
# Returns None if the alarm is already in the requested state.
result = client.create_or_update_alarm(clear_request, ignore_conflict=True)
if result is None:
    print("No state change needed (alarm already in requested state)")
else:
    print(f"Alarm cleared successfully: {result}")

# Delete the alarm by its instance ID
client.delete_alarm(instance_id=id)
