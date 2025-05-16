import pytest
from typing import List

from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.test_plans import TestPlansClient
from nisystemlink.clients.test_plan.test_plans.models import (
    CreateTestPlanRequestBodyContent,
    CreateTestPlansRequest,
    CreateTestPlansResponse,
    DeleteTestPlansRequest,
    State,
    TestPlan,
    UpdateTestPlansRequest,
    UpdateTestPlanRequestBodyContent,
    ScheduleTestPlansRequest,
    ScheduleTestPlansResponse,
    ScheduleTestPlanRequestBodyContent,
    QueryTestPlansRequest,
    QueryTestPlansResponse
)


@pytest.fixture(scope="class")
def test_plan_create() -> CreateTestPlansRequest:
    """Fixture to create create test plan object."""

    testPlan = CreateTestPlansRequest(
        testPlans=[
            CreateTestPlanRequestBodyContent(
                name="Sample Test Plan", state="NEW", partNumber="px40482"
            )
        ]
    )

    return testPlan


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestPlansClient:
    """Fixture to create a TestPlansClient instance"""
    return TestPlansClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestTestPlans:
    def test__create_and_delete_test_plan__returns_created_and_deleted_test_plans(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(testplans=test_plan_create)
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        delete_test_plan_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        delete_test_plan_response = client.delete_test_plans(ids=delete_test_plan_request)

        assert created_test_plan is not None
        assert created_test_plan.name == "Sample Test Plan"
        assert created_test_plan.state == State.New
        assert created_test_plan.partNumber == "px40482"
        assert created_test_plan.id == delete_test_plan_response.deletedTestPlanIds[0]

    def test__get_test_plan__returns_get_test_plan(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(testplans=test_plan_create)
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        get_test_plan_response: TestPlan = client.get_test_plan(created_test_plan.id)

        delete_request = DeleteTestPlansRequest(ids=[create_test_plan_response.createdTestPlans[0].id])
        client.delete_test_plans(ids=delete_request)

        assert get_test_plan_response is not None
        assert isinstance(get_test_plan_response, TestPlan)
        assert get_test_plan_response.id == created_test_plan.id

    def test__update_test_plan__returns_updated_test_plan(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(testplans=test_plan_create)
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        update_request = UpdateTestPlansRequest(
            testPlans=[
                UpdateTestPlanRequestBodyContent(
                    id=created_test_plan.id,
                    name= "Updated Test Plan",
                )
            ]
        )
        update_test_plan_response = client.update_test_plan(test_plans=update_request)

        delete_request = DeleteTestPlansRequest(ids=[create_test_plan_response.createdTestPlans[0].id])
        client.delete_test_plans(ids=delete_request)

        assert update_test_plan_response is not None
        updated_test_plan = update_test_plan_response.updated_test_plans[0]
        assert updated_test_plan.id == created_test_plan.id
        assert updated_test_plan.name == "Updated Test Plan"

    def test__schedule_test_plan__returns_scheduled_test_plan(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(testplans=test_plan_create)
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        schedule_request = ScheduleTestPlansRequest(
            test_plans=[
                ScheduleTestPlanRequestBodyContent(
                    id=created_test_plan.id,
                    planned_start_date_time="2025-05-20T15:07:42.527Z",
                    estimated_end_date_time="2025-05-20T15:07:42.527Z",
                    system_id="fake-system"
                )
            ]
        )
        schedule_test_plan_response = client.schedule_test_plan(schedule=schedule_request)

        delete_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        client.delete_test_plans(ids=delete_request)

        assert schedule_test_plan_response is not None
        scheduled_test_plan = schedule_test_plan_response.scheduled_test_plans[0]
        assert scheduled_test_plan.id == created_test_plan.id
        assert scheduled_test_plan.plannedStartDateTime == "2025-05-20T15:07:42.527Z"
        assert scheduled_test_plan.systemId == "fake-system"

    def test__query_test_plans__return_queried_test_plan(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(testplans=test_plan_create)
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        query_test_plans_request = QueryTestPlansRequest(
            filter = "id == {created_test_plan.id}",
            return_count = True
        )
        queried_test_plans_response = client.query_test_plans(query = query_test_plans_request)

        delete_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        client.delete_test_plans(ids=delete_request)

        assert queried_test_plans_response is not None
        assert queried_test_plans_response.test_plans[0].id == created_test_plan.id
        assert queried_test_plans_response.total_count > 0
    
