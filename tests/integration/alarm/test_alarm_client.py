import uuid
from datetime import datetime, timezone
from typing import List

import pytest
from nisystemlink.clients.alarm import AlarmClient
from nisystemlink.clients.alarm.models import (
    AcknowledgeByInstanceIdRequest,
    AcknowledgeByInstanceIdResponse,
    CreateOrUpdateAlarmRequest,
    CreateOrUpdateAlarmResponse,
    DeleteByInstanceIdRequest,
    DeleteByInstanceIdResponse,
    QueryWithFilterRequest,
    QueryWithFilterResponse,
)
from nisystemlink.clients.alarm.models._alarm import AlarmTransitionType
from nisystemlink.clients.alarm.models._create_or_update_alarm_request import (
    CreateAlarmTransition,
)
from nisystemlink.clients.alarm.models._query_alarms_request import (
    AlarmOrderBy,
    TransitionInclusionOption,
)
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> AlarmClient:
    """Fixture to create an AlarmClient instance."""
    return AlarmClient(enterprise_config)


@pytest.fixture
def unique_identifier() -> str:
    """Unique alarm id for this test."""
    alarm_id = uuid.uuid1().hex
    return alarm_id


@pytest.fixture
def create_alarms(client: AlarmClient):
    """Fixture to return a factory that creates alarms."""
    created_instance_ids: List[str] = []

    def _create_alarms(
        alarm_id: str,
        severity_level: int = 3,
        condition: str = "Test Condition",
    ) -> CreateOrUpdateAlarmResponse:
        request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id,
            transition=CreateAlarmTransition(
                transition_type=AlarmTransitionType.SET,
                occurred_at=datetime.now(timezone.utc),
                severity_level=severity_level,
                condition=condition,
            ),
        )
        response = client.create_or_update_alarm(request)
        created_instance_ids.append(response.instance_id)
        return response

    yield _create_alarms

    if created_instance_ids:
        client.delete_instances_by_instance_id(
            DeleteByInstanceIdRequest(instance_ids=created_instance_ids)
        )


@pytest.mark.integration
@pytest.mark.enterprise
class TestAlarmClient:
    def test__create_single_alarm__one_alarm_created_with_right_field_values(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        alarm_id = unique_identifier
        severity_level = 3
        condition = "Test Condition"

        response: CreateOrUpdateAlarmResponse = create_alarms(alarm_id)

        assert response is not None
        assert response.instance_id is not None

        alarm = client.get_alarm(response.instance_id)
        assert alarm.alarm_id == alarm_id
        assert alarm.current_severity_level == severity_level
        assert alarm.active is True
        assert alarm.clear is False

    def test__create_single_alarm_and_query_alarms__at_least_one_alarm_returned(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_alarms(unique_identifier)

        query_request = QueryWithFilterRequest(filter=f'alarmId="{unique_identifier}"')
        query_response = client.query_alarms(query_request)

        assert query_response is not None
        assert len(query_response.alarms) >= 1

    def test__create_multiple_alarms_and_query_alarms_with_take__only_take_returned(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_alarms(unique_identifier, severity_level=3)
        create_alarms(unique_identifier, severity_level=4)

        query_request = QueryWithFilterRequest(take=1)
        query_response = client.query_alarms(query_request)

        assert query_response is not None
        assert len(query_response.alarms) == 1

    def test__create_multiple_alarms_and_query_alarms_with_count__at_least_one_count(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_alarms(unique_identifier, severity_level=3)
        create_alarms(unique_identifier, severity_level=4)

        query_request = QueryWithFilterRequest(return_count=True)
        query_response: QueryWithFilterResponse = client.query_alarms(query_request)

        assert query_response is not None
        assert query_response.total_count is not None
        assert query_response.total_count >= 1

    def test__get_alarm_by_instance_id__alarm_matches_expected(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        alarm_id = unique_identifier
        create_response: CreateOrUpdateAlarmResponse = create_alarms(alarm_id)
        instance_id = create_response.instance_id

        alarm = client.get_alarm(instance_id)

        assert alarm is not None
        assert alarm.alarm_id == alarm_id

    def test__query_alarm_by_alarm_id__matches_expected(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        alarm_id = unique_identifier
        create_response: CreateOrUpdateAlarmResponse = create_alarms(alarm_id)
        assert create_response is not None

        query_request = QueryWithFilterRequest(
            filter=f'alarmId="{alarm_id}"', return_count=True
        )
        query_response: QueryWithFilterResponse = client.query_alarms(query_request)

        assert query_response.total_count == 1
        assert query_response.alarms[0].alarm_id == alarm_id

    def test__acknowledge_single_alarm__alarm_acknowledged(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_response = create_alarms(unique_identifier)
        instance_id = create_response.instance_id

        ack_request = AcknowledgeByInstanceIdRequest(instance_ids=[instance_id])
        ack_response: AcknowledgeByInstanceIdResponse = (
            client.acknowledge_instances_by_instance_id(ack_request)
        )

        assert ack_response is not None
        assert instance_id in ack_response.acknowledged
        assert len(ack_response.failed) == 0

    def test__acknowledge_multiple_alarms__all_acknowledged(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        instance_id1 = create_alarms(unique_identifier, severity_level=3).instance_id
        instance_id2 = create_alarms(unique_identifier, severity_level=4).instance_id

        ack_request = AcknowledgeByInstanceIdRequest(
            instance_ids=[instance_id1, instance_id2]
        )
        ack_response: AcknowledgeByInstanceIdResponse = (
            client.acknowledge_instances_by_instance_id(ack_request)
        )

        assert ack_response is not None
        assert instance_id1 in ack_response.acknowledged
        assert instance_id2 in ack_response.acknowledged
        assert len(ack_response.failed) == 0

    def test__acknowledge_alarm_with_force_clear__alarm_cleared(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_response = create_alarms(unique_identifier)
        instance_id = create_response.instance_id

        ack_request = AcknowledgeByInstanceIdRequest(
            instance_ids=[instance_id], force_clear=True
        )
        ack_response: AcknowledgeByInstanceIdResponse = (
            client.acknowledge_instances_by_instance_id(ack_request)
        )

        assert ack_response is not None
        assert instance_id in ack_response.acknowledged

        alarm = client.get_alarm(instance_id)
        assert alarm.clear is True

    def test__delete_single_alarm__alarm_deleted(
        self, client: AlarmClient, unique_identifier
    ):
        alarm_id = unique_identifier
        request = CreateOrUpdateAlarmRequest(
            alarm_id=alarm_id,
            transition=CreateAlarmTransition(
                transition_type=AlarmTransitionType.SET,
                occurred_at=datetime.now(timezone.utc),
                severity_level=3,
                condition="Test Condition",
            ),
        )
        create_response = client.create_or_update_alarm(request)
        instance_id = create_response.instance_id

        client.delete_alarm(instance_id)

        query_request = QueryWithFilterRequest(filter=f'alarmId="{alarm_id}"')
        query_response = client.query_alarms(query_request)
        assert len(query_response.alarms) == 0

    def test__delete_multiple_alarms__all_deleted(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        instance_id1 = create_alarms(unique_identifier, severity_level=3).instance_id
        instance_id2 = create_alarms(unique_identifier, severity_level=4).instance_id

        delete_request = DeleteByInstanceIdRequest(
            instance_ids=[instance_id1, instance_id2]
        )
        delete_response: DeleteByInstanceIdResponse = (
            client.delete_instances_by_instance_id(delete_request)
        )

        print(delete_response)
        
        assert delete_response is not None
        assert instance_id1 in delete_response.deleted
        assert instance_id2 in delete_response.deleted

    def test__update_alarm_severity__severity_updated(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_alarms(unique_identifier)

        update_request = CreateOrUpdateAlarmRequest(
            alarm_id=unique_identifier,
            transition=CreateAlarmTransition(
                transition_type=AlarmTransitionType.SET,
                occurred_at=datetime.now(timezone.utc),
                severity_level=5,
                condition="Updated Condition",
            ),
        )
        update_response = client.create_or_update_alarm(update_request)

        assert update_response is not None
        alarm = client.get_alarm(update_response.instance_id)
        assert alarm.current_severity_level == 5

    def test__clear_alarm__alarm_cleared(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_alarms(unique_identifier)

        clear_request = CreateOrUpdateAlarmRequest(
            alarm_id=unique_identifier,
            transition=CreateAlarmTransition(
                transition_type=AlarmTransitionType.CLEAR,
                occurred_at=datetime.now(timezone.utc),
                severity_level=0,
                condition="Cleared",
            ),
        )
        clear_response = client.create_or_update_alarm(clear_request)

        assert clear_response is not None
        alarm = client.get_alarm(clear_response.instance_id)
        assert alarm.clear is True

    def test__query_alarms_with_order_by_descending__alarms_ordered(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_alarms(unique_identifier, severity_level=3)
        create_alarms(unique_identifier, severity_level=4)

        query_request = QueryWithFilterRequest(
            order_by=AlarmOrderBy.UPDATED_AT,
            order_by_descending=True,
        )
        query_response = client.query_alarms(query_request)

        assert query_response is not None
        assert len(query_response.alarms) >= 1
        for i in range(len(query_response.alarms) - 1):
            assert (
                query_response.alarms[i].updated_at
                >= query_response.alarms[i + 1].updated_at
            )

    def test__query_alarms_with_all_transitions__transitions_included(
        self, client: AlarmClient, create_alarms, unique_identifier
    ):
        create_alarms(unique_identifier)

        update_request = CreateOrUpdateAlarmRequest(
            alarm_id=unique_identifier,
            transition=CreateAlarmTransition(
                transition_type=AlarmTransitionType.SET,
                occurred_at=datetime.now(timezone.utc),
                severity_level=4,
                condition="Second SET",
            ),
        )
        client.create_or_update_alarm(update_request)

        query_request = QueryWithFilterRequest(
            filter=f'alarmId="{unique_identifier}"',
            transition_inclusion_option=TransitionInclusionOption.ALL,
        )
        query_response = client.query_alarms(query_request)

        assert query_response is not None
        assert len(query_response.alarms) == 1
        assert len(query_response.alarms[0].transitions) == 2
