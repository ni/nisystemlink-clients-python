import uuid
from datetime import datetime, timezone
from typing import Callable, Generator, List

import pytest
from nisystemlink.clients.alarm import AlarmClient
from nisystemlink.clients.alarm.models import (
    AcknowledgeAlarmsResponse,
    AlarmOrderBy,
    AlarmSeverityLevel,
    AlarmTransitionType,
    ClearAlarmTransition,
    CreateOrUpdateAlarmRequest,
    DeleteAlarmsResponse,
    QueryAlarmsWithFilterRequest,
    QueryAlarmsWithFilterResponse,
    SetAlarmTransition,
    TransitionInclusionOption,
)
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> AlarmClient:
    """Fixture to create an AlarmClient instance."""
    return AlarmClient(enterprise_config)


@pytest.fixture
def unique_identifier() -> Callable[[], str]:
    """Unique alarm id for this test."""

    def _unique_identifier() -> str:
        return uuid.uuid1().hex

    return _unique_identifier


@pytest.fixture
def create_alarms(
    client: AlarmClient,
) -> Generator[Callable[[str, int, str], str], None, None]:
    """Fixture to return a factory that creates alarms.

    Returns instance_id (referred to as 'id' in tests) for each created alarm.
    """
    created_ids: List[str] = []

    def _create_alarms(
        alarm_id: str,
        severity_level: int = 3,
        condition: str = "Test Condition",
    ) -> str:
        """Create an alarm and return its instance_id."""
        request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id,
            transition=SetAlarmTransition(
                occurred_at=datetime.now(timezone.utc),
                severity_level=severity_level,
                condition=condition,
            ),
        )
        id = client.create_or_update_alarm(request)
        created_ids.append(id)
        return id

    yield _create_alarms

    if created_ids:
        client.delete_alarms(ids=created_ids)


@pytest.mark.integration
@pytest.mark.enterprise
class TestAlarmClient:

    def test__create_single_alarm__one_alarm_created_with_right_field_values(
        self, client: AlarmClient, unique_identifier: Callable[[], str]
    ):
        alarm_id = unique_identifier()
        occurred_at = datetime.now(timezone.utc)

        # Create alarm with all fields populated
        request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id,
            workspace=None,  # Use default workspace
            transition=SetAlarmTransition(
                occurred_at=occurred_at,
                severity_level=AlarmSeverityLevel.HIGH,
                value="85.5",
                condition="Temperature exceeded threshold",
                short_text="High temp",
                detail_text="Temperature sensor reading exceeded the configured threshold of 80°C",
                keywords=["temperature", "sensor", "critical"],
                properties={"sensor_id": "temp_001", "location": "server_room"},
            ),
            notification_strategy_ids=[],
            created_by="test_automation",
            channel="sensors/temperature/room1",
            resource_type="temperature_sensor",
            display_name="Server Room Temperature",
            description="Monitors temperature in server room",
            keywords=["monitoring", "infrastructure"],
            properties={"department": "IT", "priority": "high"},
        )

        id = client.create_or_update_alarm(request)
        assert id is not None
        assert isinstance(id, str)
        assert len(id) > 0

        # Get alarm and verify all fields
        alarm = client.get_alarm(id)
        assert alarm.instance_id == id
        assert alarm.alarm_id == alarm_id
        assert alarm.workspace is not None
        assert alarm.active is True
        assert alarm.clear is False
        assert alarm.acknowledged is False
        assert alarm.acknowledged_at is None
        assert alarm.acknowledged_by is None
        assert alarm.occurred_at is not None
        assert alarm.updated_at is not None
        assert alarm.created_by == "test_automation"
        assert len(alarm.transitions) >= 1
        assert alarm.transition_overflow_count == 0
        assert isinstance(alarm.notification_strategy_ids, List)
        assert alarm.current_severity_level == 3
        assert alarm.highest_severity_level == 3
        assert alarm.most_recent_set_occurred_at is not None
        assert alarm.most_recent_transition_occurred_at is not None
        assert alarm.channel == "sensors/temperature/room1"
        assert alarm.condition == "Temperature exceeded threshold"
        assert alarm.display_name == "Server Room Temperature"
        assert alarm.description == "Monitors temperature in server room"
        assert "monitoring" in alarm.keywords
        assert "infrastructure" in alarm.keywords
        assert isinstance(alarm.notes, List)
        assert "department" in alarm.properties
        assert alarm.properties["department"] == "IT"
        assert alarm.resource_type == "temperature_sensor"

        # Verify transition fields
        transition = alarm.transitions[0]
        assert transition.transition_type == AlarmTransitionType.SET
        assert transition.occurred_at is not None
        assert transition.severity_level == 3
        assert transition.value == "85.5"
        assert transition.condition == "Temperature exceeded threshold"
        assert transition.short_text == "High temp"
        assert (
            transition.detail_text
            == "Temperature sensor reading exceeded the configured threshold of 80°C"
        )
        assert "temperature" in transition.keywords
        assert "sensor_id" in transition.properties

        # Cleanup
        client.delete_alarm(id)

    def test__query_alarms_with_all_fields__returns_complete_response(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        # Create two alarms with different severity levels
        alarm_id_1 = unique_identifier()
        alarm_id_2 = unique_identifier()
        create_alarms(alarm_id_1, 3, "Condition 1")
        create_alarms(alarm_id_2, 4, "Condition 2")

        # Add another transition to the first alarm
        update_request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id_1,
            transition=SetAlarmTransition(
                occurred_at=datetime.now(timezone.utc),
                severity_level=AlarmSeverityLevel.CRITICAL,
                condition="Condition 3",
            ),
        )
        client.create_or_update_alarm(update_request)

        # Query with all available fields, order by descending, and ALL transitions
        query_request = QueryAlarmsWithFilterRequest(
            filter=f'alarmId="{alarm_id_1}" OR alarmId="{alarm_id_2}"',
            substitutions=None,
            return_most_recently_occurred_only=False,
            transition_inclusion_option=TransitionInclusionOption.ALL,
            reference_time=None,
            take=10,
            order_by=AlarmOrderBy.UPDATED_AT,
            order_by_descending=True,
            continuation_token=None,
            return_count=True,
        )
        query_response: QueryAlarmsWithFilterResponse = client.query_alarms(
            query_request
        )

        # Assert all response fields
        assert query_response is not None
        assert isinstance(query_response.alarms, List)
        assert len(query_response.alarms) == 2
        assert query_response.total_count is not None
        assert query_response.total_count == 2
        assert hasattr(query_response, "continuation_token")

        # Verify order_by_descending works (alarm_id_1 was updated last, should be first)
        for i in range(len(query_response.alarms) - 1):
            assert (
                query_response.alarms[i].updated_at
                >= query_response.alarms[i + 1].updated_at
            )

        # Verify all transitions are included (TransitionInclusionOption.ALL) for alarm_id_1
        alarm_1_result = next(
            a for a in query_response.alarms if a.alarm_id == alarm_id_1
        )
        assert len(alarm_1_result.transitions) == 2

    def test__create_multiple_alarms_and_query_alarms_with_take__only_take_returned(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        create_alarms(unique_identifier(), 3, "Test Condition")
        create_alarms(unique_identifier(), 4, "Test Condition")

        query_request = QueryAlarmsWithFilterRequest(take=1)
        query_response = client.query_alarms(query_request)

        assert query_response is not None
        assert len(query_response.alarms) == 1

    def test__query_alarm_by_alarm_id__matches_expected(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        alarm_id = unique_identifier()
        id = create_alarms(alarm_id, 3, "Test Condition")
        assert id is not None

        query_request = QueryAlarmsWithFilterRequest(
            filter=f'alarmId="{alarm_id}"', return_count=True
        )
        query_response: QueryAlarmsWithFilterResponse = client.query_alarms(
            query_request
        )

        assert query_response.total_count == 1
        assert query_response.alarms[0].alarm_id == alarm_id

    def test__acknowledge_alarm__verifies_all_response_fields(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        # Create multiple alarms
        id1 = create_alarms(unique_identifier(), 3, "Test Condition")
        id2 = create_alarms(unique_identifier(), 4, "Test Condition")
        non_existent_id = unique_identifier()

        # Acknowledge with mix of valid and invalid IDs
        ack_response: AcknowledgeAlarmsResponse = client.acknowledge_alarms(
            ids=[id1, id2, non_existent_id], force_clear=False
        )

        # Assert all response fields
        assert ack_response is not None
        assert isinstance(ack_response.acknowledged, List)
        assert isinstance(ack_response.failed, List)
        assert id1 in ack_response.acknowledged
        assert id2 in ack_response.acknowledged
        assert non_existent_id in ack_response.failed
        assert len(ack_response.acknowledged) == 2
        assert len(ack_response.failed) == 1
        assert hasattr(ack_response, "error")

        # Verify alarms were acknowledged
        alarm1 = client.get_alarm(id1)
        assert alarm1.acknowledged is True
        assert alarm1.acknowledged_at is not None
        assert alarm1.acknowledged_by is not None

    def test__acknowledge_alarm_with_force_clear__alarm_cleared(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        id = create_alarms(unique_identifier(), 3, "Test Condition")

        ack_response: AcknowledgeAlarmsResponse = client.acknowledge_alarms(
            ids=[id], force_clear=True
        )

        assert ack_response is not None
        assert id in ack_response.acknowledged

        alarm = client.get_alarm(id)
        assert alarm.clear is True

    def test__delete_alarm__returns_none(
        self, client: AlarmClient, unique_identifier: Callable[[], str]
    ):
        alarm_id = unique_identifier()
        request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id,
            transition=SetAlarmTransition(
                occurred_at=datetime.now(timezone.utc),
                severity_level=AlarmSeverityLevel.HIGH,
                condition="Test Condition",
            ),
        )
        id = client.create_or_update_alarm(request)

        # Delete returns None on success
        result = client.delete_alarm(id)
        assert result is None

        # Verify alarm is deleted
        query_request = QueryAlarmsWithFilterRequest(filter=f'alarmId="{alarm_id}"')
        query_response = client.query_alarms(query_request)
        assert len(query_response.alarms) == 0

    def test__delete_alarms__verifies_all_response_fields(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        alarm_id1 = unique_identifier()
        alarm_id2 = unique_identifier()
        # Create multiple alarms with different alarm IDs
        id1 = create_alarms(alarm_id1, 3, "Test Condition")
        id2 = create_alarms(alarm_id2, 4, "Test Condition")
        non_existent_id = unique_identifier()

        # Delete with mix of valid and invalid IDs
        delete_response: DeleteAlarmsResponse = client.delete_alarms(
            ids=[id1, id2, non_existent_id]
        )

        # Assert all response fields
        assert delete_response is not None
        assert isinstance(delete_response.deleted, List)
        assert isinstance(delete_response.failed, List)
        assert id1 in delete_response.deleted
        assert id2 in delete_response.deleted
        assert non_existent_id in delete_response.failed
        assert len(delete_response.deleted) == 2
        assert len(delete_response.failed) == 1
        assert hasattr(delete_response, "error")

        # Verify alarms were deleted
        query_request = QueryAlarmsWithFilterRequest(
            filter=f'alarmId="{alarm_id1}" or alarmId="{alarm_id2}"'
        )
        query_response = client.query_alarms(query_request)
        assert len(query_response.alarms) == 0

    def test__update_alarm_severity__severity_updated(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        alarm_id = unique_identifier()
        create_alarms(alarm_id, 3, "Test Condition")

        update_request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id,
            transition=SetAlarmTransition(
                occurred_at=datetime.now(timezone.utc),
                severity_level=AlarmSeverityLevel.CRITICAL,
                condition="Updated Condition",
            ),
        )
        id = client.create_or_update_alarm(update_request)

        assert id is not None
        alarm = client.get_alarm(id)
        assert alarm.current_severity_level == AlarmSeverityLevel.CRITICAL

    def test__clear_alarm__alarm_cleared(
        self,
        client: AlarmClient,
        create_alarms: Callable[[str, int, str], str],
        unique_identifier: Callable[[], str],
    ):
        alarm_id = unique_identifier()
        create_alarms(alarm_id, 3, "Test Condition")

        clear_request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id,
            transition=ClearAlarmTransition(
                occurred_at=datetime.now(timezone.utc),
                condition="Cleared",
            ),
        )
        id = client.create_or_update_alarm(clear_request)

        assert id is not None
        alarm = client.get_alarm(id)
        assert alarm.clear is True

    def test__get_alarm_with_invalid_instance_id__raises_ApiException_NotFound(
        self, client: AlarmClient
    ):
        with pytest.raises(ApiException):
            client.get_alarm("invalid_instance_id")

    def test__delete_alarm_with_invalid_instance_id__raises_ApiException_NotFound(
        self, client: AlarmClient
    ):
        with pytest.raises(ApiException):
            client.delete_alarm("invalid_instance_id")

    def test__query_alarms_with_invalid_filter_syntax__raises_ApiException_BadRequest(
        self, client: AlarmClient
    ):
        query_request = QueryAlarmsWithFilterRequest(filter="invalid filter syntax")
        with pytest.raises(ApiException, match="Bad Request"):
            client.query_alarms(query_request)

    def test__query_alarm_with_non_existent_alarm_id__returns_empty_list(
        self, client: AlarmClient, unique_identifier: Callable[[], str]
    ):
        non_existent_alarm_id = f"non_existent_{unique_identifier()}"
        query_request = QueryAlarmsWithFilterRequest(
            filter=f'alarmId="{non_existent_alarm_id}"'
        )
        query_response = client.query_alarms(query_request)

        assert query_response is not None
        assert len(query_response.alarms) == 0

    def test__create_alarm_with_invalid_severity__raises_ApiException_BadRequest(
        self, client: AlarmClient, unique_identifier: Callable[[], str]
    ):
        request = CreateOrUpdateAlarmRequest(
            alarm_id=unique_identifier(),
            transition=SetAlarmTransition(
                occurred_at=datetime.now(timezone.utc),
                severity_level=-999,
                condition="Invalid Severity",
            ),
        )
        with pytest.raises(ApiException, match="Bad Request"):
            client.create_or_update_alarm(request)
