from datetime import datetime
from typing import List

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan import TestPlanClient
from nisystemlink.clients.test_plan.models import (
    CreateTestPlanRequest,
    CreateTestPlansPartialSuccessResponse,
    CreateTestPlanTemplatePartialSuccessResponse,
    CreateTestPlanTemplateRequest,
    Dashboard,
    Job,
    JobExecution,
    ManualExecution,
    QueryTestPlansRequest,
    QueryTestPlanTemplatesRequest,
    ScheduleTestPlanRequest,
    ScheduleTestPlansRequest,
    State,
    TestPlan,
    TestPlanField,
    TestPlanTemplate,
    TestPlanTemplateField,
    UpdateTestPlanRequest,
    UpdateTestPlansRequest,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestPlanClient:
    """Fixture to create a TestPlansClient instance"""
    return TestPlanClient(enterprise_config)


@pytest.fixture
def create_test_plans(client: TestPlanClient):
    """Fixture to return a factory that create test plans."""
    responses: List[CreateTestPlansPartialSuccessResponse] = []

    def _create_test_plans(
        new_test_plans: List[CreateTestPlanRequest],
    ) -> CreateTestPlansPartialSuccessResponse:
        response = client.create_test_plans(test_plans=new_test_plans)
        responses.append(response)
        return response

    yield _create_test_plans

    created_test_plans: List[TestPlan] = []
    for response in responses:
        if response.created_test_plans:
            created_test_plans += response.created_test_plans

    client.delete_test_plans(
        ids=[
            test_plans.id
            for test_plans in created_test_plans
            if test_plans.id is not None
        ]
    )


@pytest.fixture
def create_test_plan_templates(client: TestPlanClient):
    """Fixture to return a factory that create test plan templates."""
    responses: List[CreateTestPlanTemplatePartialSuccessResponse] = []

    def _create_test_plan_templates(
        new_test_plan_templates: List[CreateTestPlanTemplateRequest],
    ) -> CreateTestPlanTemplatePartialSuccessResponse:
        response = client.create_test_plan_templates(
            test_plan_templates=new_test_plan_templates
        )
        responses.append(response)
        return response

    yield _create_test_plan_templates

    created_test_plan_templates: List[TestPlanTemplate] = []
    for response in responses:
        if response.created_test_plan_templates:
            created_test_plan_templates = (
                created_test_plan_templates + response.created_test_plan_templates
            )
    client.delete_test_plan_templates(
        ids=[
            test_plan_template.id
            for test_plan_template in created_test_plan_templates
            if test_plan_template.id is not None
        ]
    )


@pytest.mark.integration
@pytest.mark.enterprise
class TestTestPlanClient:

    _workspace = "2300760d-38c4-48a1-9acb-800260812337"

    _dashboard = Dashboard(
        id="DashBoardId", variables={"product": "PXIe-4080", "location": "Lab1"}
    )

    _execution_actions = [
        ManualExecution(action="boot", type="MANUAL"),
        JobExecution(
            action="run",
            type="JOB",
            jobs=[
                Job(
                    functions=["run_test_suite"],
                    arguments=[["test_suite.py"]],
                    metadata={"env": "staging"},
                )
            ],
            systemId="system-001",
        ),
    ]

    _test_plan_create = [
        CreateTestPlanRequest(
            name="Python integration test plan",
            state="NEW",
            description="Test plan for verifying integration flow",
            assigned_to="test.user@example.com",
            estimated_duration_in_seconds=86400,
            properties={"env": "staging", "priority": "high"},
            part_number="px40482",
            dut_id="Sample-Dut_Id",
            test_program="TP-Integration-001",
            system_filter="os:linux AND arch:x64",
            workspace=_workspace,
            file_ids_from_template=["file1", "file2"],
            dashboard=_dashboard,
            execution_actions=_execution_actions,
        )
    ]
    """create test plan request object."""

    _create_test_plan_template_request = [
        CreateTestPlanTemplateRequest(
            name="Python integration test plan template",
            template_group="sample template group",
            product_families=["FamilyA", "FamilyB"],
            part_numbers=["PN-1001", "PN-1002"],
            summary="Template for running integration test plans",
            description="This template defines execution steps for integration workflows.",
            test_program="TP-INT-002",
            estimated_duration_in_seconds=86400,
            system_filter="os:linux AND arch:x64",
            execution_actions=_execution_actions,
            file_ids=["file1", "file2"],
            workspace=_workspace,
            properties={"env": "staging", "priority": "high"},
            dashboard=_dashboard,
        )
    ]
    """create test plan template request object."""

    def test__create_and_delete_test_plan__returns_created_and_deleted_test_plans(
        self, client: TestPlanClient, create_test_plans
    ):
        create_test_plan_template_response = client.create_test_plan_templates(
            test_plan_templates=self._create_test_plan_template_request
        )

        template_id = (
            create_test_plan_template_response.created_test_plan_templates[0].id
            if create_test_plan_template_response.created_test_plan_templates
            and create_test_plan_template_response.created_test_plan_templates[0].id
            else None
        )

        assert template_id is not None

        test_plan_request = self._test_plan_create
        test_plan_request[0].template_id = template_id

        create_test_plan_response = create_test_plans(test_plan_request)

        assert create_test_plan_response.created_test_plans is not None

        created_test_plan = create_test_plan_response.created_test_plans[0]

        get_test_plan_response: TestPlan = client.get_test_plan(created_test_plan.id)

        client.delete_test_plan_templates(ids=[template_id])

        assert created_test_plan is not None
        assert created_test_plan.name == "Python integration test plan"
        assert created_test_plan.state == State.NEW
        assert created_test_plan.part_number == "px40482"
        assert get_test_plan_response is not None
        assert get_test_plan_response.name == "Python integration test plan"

    def test__get_test_plan__returns_get_test_plan(
        self, client: TestPlanClient, create_test_plans
    ):
        create_test_plan_response = create_test_plans(self._test_plan_create)

        assert create_test_plan_response.created_test_plans is not None

        created_test_plan = create_test_plan_response.created_test_plans[0]

        get_test_plan_response: TestPlan = client.get_test_plan(created_test_plan.id)

        assert get_test_plan_response is not None
        assert isinstance(get_test_plan_response, TestPlan)
        assert get_test_plan_response.id == created_test_plan.id

    def test__update_test_plan__returns_updated_test_plan(
        self, client: TestPlanClient, create_test_plans
    ):
        create_test_plan_response = create_test_plans(self._test_plan_create)

        assert create_test_plan_response.created_test_plans is not None

        created_test_plan = create_test_plan_response.created_test_plans[0]

        update_test_plans_request = UpdateTestPlansRequest(
            test_plans=[
                UpdateTestPlanRequest(
                    id=created_test_plan.id,
                    name="Updated Test Plan",
                )
            ]
        )
        update_test_plans_response = client.update_test_plans(
            update_request=update_test_plans_request
        )

        assert update_test_plans_response.updated_test_plans is not None

        updated_test_plan = update_test_plans_response.updated_test_plans[0]
        assert updated_test_plan.id == created_test_plan.id
        assert updated_test_plan.name == "Updated Test Plan"

    def test__schedule_test_plan__returns_scheduled_test_plan(
        self, client: TestPlanClient, create_test_plans
    ):
        create_test_plan_response = create_test_plans(self._test_plan_create)

        assert create_test_plan_response.created_test_plans is not None

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

        assert schedule_test_plans_response.scheduled_test_plans is not None

        scheduled_test_plan = schedule_test_plans_response.scheduled_test_plans[0]
        assert scheduled_test_plan.id == created_test_plan.id
        assert scheduled_test_plan.planned_start_date_time == datetime.strptime(
            "2025-05-20T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert scheduled_test_plan.system_id == "fake-system"

    def test__query_test_plans__return_queried_test_plan(
        self, client: TestPlanClient, create_test_plans
    ):
        create_test_plan_response = create_test_plans(self._test_plan_create)

        assert create_test_plan_response.created_test_plans is not None

        created_test_plan = create_test_plan_response.created_test_plans[0]

        query_test_plans_request = QueryTestPlansRequest(
            filter=f'id = "{created_test_plan.id}"', return_count=True
        )
        queried_test_plans_response = client.query_test_plans(
            query_request=query_test_plans_request
        )

        assert queried_test_plans_response is not None
        assert queried_test_plans_response.test_plans[0].id == created_test_plan.id
        assert queried_test_plans_response.total_count is not None
        assert queried_test_plans_response.total_count > 0

    def test__query_test_plans_with_projections__returns_the_test_plans_with_projected_properties(
        self, client: TestPlanClient, create_test_plans
    ):
        create_test_plan_response = create_test_plans(self._test_plan_create)

        assert create_test_plan_response.created_test_plans is not None

        created_test_plan = create_test_plan_response.created_test_plans[0]
        query_test_plans_request = QueryTestPlansRequest(
            filter=f'id = "{created_test_plan.id}"',
            projection=[TestPlanField.ID, TestPlanField.NAME],
            take=1,
        )
        response = client.query_test_plans(query_request=query_test_plans_request)

        assert response is not None
        test_plan = response.test_plans[0]
        assert (
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
        )

    def test__create_test_plan_template__returns_created_test_plan_template(
        self, client: TestPlanClient, create_test_plan_templates
    ):
        create_test_plan_template_response = create_test_plan_templates(
            self._create_test_plan_template_request
        )

        template_id = (
            create_test_plan_template_response.created_test_plan_templates[0].id
            if create_test_plan_template_response.created_test_plan_templates
            and create_test_plan_template_response.created_test_plan_templates[0].id
            else None
        )

        assert template_id is not None
        assert (
            create_test_plan_template_response.created_test_plan_templates[0].name
            == self._create_test_plan_template_request[0].name
        )

    def test__query_test_plan_template__returns_queried_test_plan_template(
        self, client: TestPlanClient, create_test_plan_templates
    ):
        create_test_plan_template_response = create_test_plan_templates(
            self._create_test_plan_template_request
        )

        template_id = (
            create_test_plan_template_response.created_test_plan_templates[0].id
            if create_test_plan_template_response.created_test_plan_templates
            and create_test_plan_template_response.created_test_plan_templates[0].id
            else None
        )

        assert template_id is not None

        query = QueryTestPlanTemplatesRequest(filter=f'id="{template_id}"', take=1)

        query_test_plan_template_response = client.query_test_plan_templates(
            query_test_plan_templates=query
        )

        assert len(query_test_plan_template_response.test_plan_templates) == 1, query
        assert (
            query_test_plan_template_response.test_plan_templates[0].id == template_id
        )

    def test__delete_test_plan_template(self, client: TestPlanClient):
        create_test_plan_template_response: (
            CreateTestPlanTemplatePartialSuccessResponse
        ) = client.create_test_plan_templates(
            test_plan_templates=self._create_test_plan_template_request
        )

        template_id = (
            create_test_plan_template_response.created_test_plan_templates[0].id
            if create_test_plan_template_response.created_test_plan_templates
            and create_test_plan_template_response.created_test_plan_templates[0].id
            else None
        )

        assert template_id is not None

        client.delete_test_plan_templates(ids=[template_id])

        query_deleted_test_plan_template_response = client.query_test_plan_templates(
            query_test_plan_templates=QueryTestPlanTemplatesRequest(
                filter=f'id="{template_id}"', take=1
            )
        )

        assert len(query_deleted_test_plan_template_response.test_plan_templates) == 0

    def test_query_test_plan_templates_with_projections__returns_test_plan_templates_with_projected_properties(
        self, client: TestPlanClient, create_test_plan_templates
    ):
        create_test_plan_template_response = create_test_plan_templates(
            self._create_test_plan_template_request
        )

        template_id = (
            create_test_plan_template_response.created_test_plan_templates[0].id
            if create_test_plan_template_response.created_test_plan_templates
            and create_test_plan_template_response.created_test_plan_templates[0].id
            else None
        )

        assert template_id is not None

        query = QueryTestPlanTemplatesRequest(
            filter=f'id="{template_id}"',
            projection=[TestPlanTemplateField.ID, TestPlanTemplateField.NAME],
            take=1,
        )
        print(query)
        response = client.query_test_plan_templates(query_test_plan_templates=query)

        assert response is not None
        test_plan_template = response.test_plan_templates[0]
        assert (
            test_plan_template.id is not None
            and test_plan_template.name is not None
            and test_plan_template.template_group is None
            and test_plan_template.product_families is None
            and test_plan_template.part_numbers is None
            and test_plan_template.summary is None
            and test_plan_template.description is None
            and test_plan_template.test_program is None
            and test_plan_template.estimated_duration_in_seconds is None
            and test_plan_template.system_filter is None
            and test_plan_template.execution_actions is None
            and test_plan_template.file_ids is None
            and test_plan_template.workspace is None
            and test_plan_template.properties is None
            and test_plan_template.dashboard is None
        )
