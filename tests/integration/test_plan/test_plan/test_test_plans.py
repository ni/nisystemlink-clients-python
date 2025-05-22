from datetime import datetime

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.test_plan import TestPlanClient
from nisystemlink.clients.test_plan.test_plan.models import (
    CreateTestPlanRequest,
    CreateTestPlansRequest,
    CreateTestPlansResponse,
    DeleteTestPlansRequest,
    QueryTestPlansRequest,
    ScheduleTestPlanRequest,
    ScheduleTestPlansRequest,
    State,
    TestPlan,
    TestPlanField,
    UpdateTestPlanRequest,
    UpdateTestPlansRequest,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestPlanClient:
    """Fixture to create a TestPlansClient instance"""
    return TestPlanClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestTestPlans:

    _test_plan_create = CreateTestPlansRequest(
        testPlans=[
            CreateTestPlanRequest(
                name="Python integration test plan", state="NEW", part_number="px40482"
            )
        ]
    )
    """create test plan object."""

    def test__create_and_delete_test_plan__returns_created_and_deleted_test_plans(
        self, client: TestPlanClient
    ):
        create_test_plan_response = client.create_test_plans(
            create_request=self._test_plan_create
        )
        created_test_plan = create_test_plan_response.created_test_plans[0]

        get_test_plan_response: TestPlan = client.get_test_plan(created_test_plan.id)

        delete_test_plan_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        client.delete_test_plans(ids=delete_test_plan_request)

        assert created_test_plan is not None
        assert created_test_plan.name == "Python integration test plan"
        assert created_test_plan.state == State.NEW
        assert created_test_plan.part_number == "px40482"
        assert get_test_plan_response is not None
        assert get_test_plan_response.name == "Python integration test plan"

    def test__get_test_plan__returns_get_test_plan(self, client: TestPlanClient):
        create_test_plan_response = client.create_test_plans(
            create_request=self._test_plan_create
        )
        created_test_plan = create_test_plan_response.created_test_plans[0]

        get_test_plan_response: TestPlan = client.get_test_plan(created_test_plan.id)

        delete_request = DeleteTestPlansRequest(
            ids=[create_test_plan_response.created_test_plans[0].id]
        )
        client.delete_test_plans(ids=delete_request)

        assert get_test_plan_response is not None
        assert isinstance(get_test_plan_response, TestPlan)
        assert get_test_plan_response.id == created_test_plan.id

    def test__update_test_plan__returns_updated_test_plan(self, client: TestPlanClient):
        create_test_plan_response = client.create_test_plans(
            create_request=self._test_plan_create
        )
        created_test_plan = create_test_plan_response.created_test_plans[0]

        update_test_plans_request = UpdateTestPlansRequest(
            testPlans=[
                UpdateTestPlanRequest(
                    id=created_test_plan.id,
                    name="Updated Test Plan",
                )
            ]
        )
        update_test_plans_response = client.update_test_plans(
            update_request=update_test_plans_request
        )

        delete_request = DeleteTestPlansRequest(
            ids=[create_test_plan_response.created_test_plans[0].id]
        )
        client.delete_test_plans(ids=delete_request)

        assert update_test_plans_response is not None
        updated_test_plan = update_test_plans_response.updated_test_plans[0]
        assert updated_test_plan.id == created_test_plan.id
        assert updated_test_plan.name == "Updated Test Plan"

    def test__schedule_test_plan__returns_scheduled_test_plan(
        self, client: TestPlanClient
    ):
        create_test_plan_response = client.create_test_plans(
            create_request=self._test_plan_create
        )
        created_test_plan = create_test_plan_response.created_test_plans[0]

        schedule_test_plans_request = ScheduleTestPlansRequest(
            test_plans=[
                ScheduleTestPlanRequest(
                    id=created_test_plan.id,
                    planned_start_date_time=datetime.strptime(
                        "2025-05-20T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    estimated_end_date_time=datetime.strptime(
                        "2025-05-22T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    system_id="fake-system",
                )
            ]
        )
        schedule_test_plans_response = client.schedule_test_plans(
            schedule_request=schedule_test_plans_request
        )

        delete_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        client.delete_test_plans(ids=delete_request)

        assert schedule_test_plans_response is not None
        scheduled_test_plan = schedule_test_plans_response.scheduled_test_plans[0]
        assert scheduled_test_plan.id == created_test_plan.id
        assert scheduled_test_plan.planned_start_date_time == datetime.strptime(
            "2025-05-20T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert scheduled_test_plan.system_id == "fake-system"

    def test__query_test_plans__return_queried_test_plan(self, client: TestPlanClient):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(
            create_request=self._test_plan_create
        )
        created_test_plan = create_test_plan_response.created_test_plans[0]

        query_test_plans_request = QueryTestPlansRequest(
            filter=f'id = "{created_test_plan.id}"', return_count=True
        )
        queried_test_plans_response = client.query_test_plans(
            query_request=query_test_plans_request
        )

        delete_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        client.delete_test_plans(ids=delete_request)

        assert queried_test_plans_response is not None
        assert queried_test_plans_response.test_plans[0].id == created_test_plan.id
        assert queried_test_plans_response.total_count > 0

    def test__query_test_plans_with_projections__returns_the_test_plans_with_projected_properties(
        self, client: TestPlanClient
    ):
        query_test_plans_request = QueryTestPlansRequest(
            projection=[TestPlanField.ID, TestPlanField.NAME]
        )
        response = client.query_test_plans(query_request=query_test_plans_request)

        assert response is not None
        assert all(
            test_plan.id is not None
            and test_plan.name is not None
            and test_plan.template_id is None
            and test_plan.state is None
            and test_plan.substate is None
            and test_plan.description is None
            and test_plan.assigned_to is None
            and test_plan.work_order_id is None
            and test_plan.work_order_name is None
            and test_plan.workspace is None
            and test_plan.created_by is None
            and test_plan.updated_at is None
            and test_plan.created_At is None
            and test_plan.updated_by is None
            and test_plan.properties is None
            and test_plan.part_number is None
            and test_plan.dut_id is None
            and test_plan.test_program is None
            and test_plan.system_filter is None
            and test_plan.fixture_ids is None
            and test_plan.system_id is None
            and test_plan.planned_start_date_time is None
            and test_plan.estimated_duration_in_seconds is None
            and test_plan.estimated_end_date_time is None
            and test_plan.file_ids_from_template is None
            and test_plan.execution_actions is None
            and test_plan.execution_history is None
            and test_plan.dashboard_url is None
            and test_plan.dashboard is None
            and test_plan.workflow is None
            for test_plan in response.test_plans
        )
