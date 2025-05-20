import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.test_plans import TestPlansClient
from nisystemlink.clients.test_plan.test_plans.models import (
    CreateTestPlanBodyContent,
    CreateTestPlansRequest,
    CreateTestPlansResponse,
    DeleteTestPlansRequest,
    QueryTestPlansRequest,
    ScheduleTestPlanBodyContent,
    ScheduleTestPlansRequest,
    State,
    TestPlan,
    TestPlanField,
    UpdateTestPlanBodyContent,
    UpdateTestPlansRequest,
)


@pytest.fixture(scope="class")
def test_plan_create() -> CreateTestPlansRequest:
    """Fixture to create create test plan object."""
    testPlan = CreateTestPlansRequest(
        testPlans=[
            CreateTestPlanBodyContent(
                name="Python integration test plan", state="NEW", partNumber="px40482"
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
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(
            testplans=test_plan_create
        )
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        get_test_plan_response: TestPlan = client.get_test_plan(created_test_plan.id)

        delete_test_plan_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        client.delete_test_plans(ids=delete_test_plan_request)

        assert created_test_plan is not None
        assert created_test_plan.name == "Python integration test plan"
        assert created_test_plan.state == State.New
        assert created_test_plan.partNumber == "px40482"
        assert get_test_plan_response is not None
        assert get_test_plan_response.name == "Python integration test plan"

    def test__get_test_plan__returns_get_test_plan(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(
            testplans=test_plan_create
        )
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        get_test_plan_response: TestPlan = client.get_test_plan(created_test_plan.id)

        delete_request = DeleteTestPlansRequest(
            ids=[create_test_plan_response.createdTestPlans[0].id]
        )
        client.delete_test_plans(ids=delete_request)

        assert get_test_plan_response is not None
        assert isinstance(get_test_plan_response, TestPlan)
        assert get_test_plan_response.id == created_test_plan.id

    def test__update_test_plan__returns_updated_test_plan(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(
            testplans=test_plan_create
        )
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        update_request = UpdateTestPlansRequest(
            testPlans=[
                UpdateTestPlanBodyContent(
                    id=created_test_plan.id,
                    name="Updated Test Plan",
                )
            ]
        )
        update_test_plan_response = client.update_test_plan(test_plans=update_request)

        delete_request = DeleteTestPlansRequest(
            ids=[create_test_plan_response.createdTestPlans[0].id]
        )
        client.delete_test_plans(ids=delete_request)

        assert update_test_plan_response is not None
        updated_test_plan = update_test_plan_response.updated_test_plans[0]
        assert updated_test_plan.id == created_test_plan.id
        assert updated_test_plan.name == "Updated Test Plan"

    def test__schedule_test_plan__returns_scheduled_test_plan(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(
            testplans=test_plan_create
        )
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        schedule_request = ScheduleTestPlansRequest(
            test_plans=[
                ScheduleTestPlanBodyContent(
                    id=created_test_plan.id,
                    planned_start_date_time="2025-05-20T15:07:42.527Z",
                    estimated_end_date_time="2025-05-20T15:07:42.527Z",
                    system_id="fake-system",
                )
            ]
        )
        schedule_test_plan_response = client.schedule_test_plan(
            schedule=schedule_request
        )

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
        create_test_plan_response: CreateTestPlansResponse = client.create_test_plans(
            testplans=test_plan_create
        )
        created_test_plan = create_test_plan_response.createdTestPlans[0]

        query_test_plans_request = QueryTestPlansRequest(
            filter=f'id = "{created_test_plan.id}"', return_count=True
        )
        queried_test_plans_response = client.query_test_plans(
            query=query_test_plans_request
        )

        delete_request = DeleteTestPlansRequest(ids=[created_test_plan.id])
        client.delete_test_plans(ids=delete_request)

        assert queried_test_plans_response is not None
        assert queried_test_plans_response.test_plans[0].id == created_test_plan.id
        assert queried_test_plans_response.total_count > 0

    def test__query_test_plans_with_projections__returns_the_test_plans_with_projected_properties(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest
    ):
        query_test_plans_request = QueryTestPlansRequest(
            projection=[TestPlanField.ID, TestPlanField.NAME]
        )
        response = client.query_test_plans(query=query_test_plans_request)

        assert response is not None
        assert all(
            test_plan.id is not None
            and test_plan.name is not None
            and test_plan.templateId is None
            and test_plan.state is None
            and test_plan.substate is None
            and test_plan.description is None
            and test_plan.assignedTo is None
            and test_plan.workOrderId is None
            and test_plan.workOrderName is None
            and test_plan.workspace is None
            and test_plan.createdBy is None
            and test_plan.updatedBy is None
            and test_plan.createdAt is None
            and test_plan.updatedAt is None
            and test_plan.properties is None
            and test_plan.partNumber is None
            and test_plan.dutId is None
            and test_plan.testProgram is None
            and test_plan.systemId is None
            and test_plan.fixtureIds is None
            and test_plan.systemFilter is None
            and test_plan.plannedStartDateTime is None
            and test_plan.estimatedEndDateTime is None
            and test_plan.estimatedDurationInSeconds is None
            and test_plan.fileIdsFromTemplate is None
            and test_plan.executionActions is None
            and test_plan.executionHistory is None
            and test_plan.dashboardUrl is None
            and test_plan.dashboard is None
            and test_plan.workflow is None
            for test_plan in response.test_plans
        )
