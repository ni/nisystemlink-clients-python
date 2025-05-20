from typing import List

import pytest

from nisystemlink.clients.core._http_configuration import HttpConfiguration

from nisystemlink.clients.test_plan.models._execution_definition import ManualExecution
from nisystemlink.clients.test_plan.test_plan_templates import TestPlanTemplateClient
from nisystemlink.clients.test_plan.test_plan_templates.models import (
    CreateTestPlanTemplatePartialSuccessResponse,
    QueryTestPlanTemplatesRequest,
    QueryTestPlanTemplatesResponse,
    TestPlanTemplateBase,
    TestPlanTemplateField,
    TestPlanTemplateResponse,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestPlanTemplateClient:
    """Fixture to create a TestPlanTemplateClient instance."""
    return TestPlanTemplateClient(enterprise_config)


@pytest.fixture
def create_test_plan_templates(client: TestPlanTemplateClient):
    """Fixture to return a factory that create test plan templates."""
    responses: List[CreateTestPlanTemplatePartialSuccessResponse] = []

    def _create_test_plan_templates(
        new_test_plan_templates: List[TestPlanTemplateBase],
    ) -> CreateTestPlanTemplatePartialSuccessResponse:
        response = client.create_test_plan_templates(
            test_plan_templates=new_test_plan_templates
        )
        responses.append(response)
        return response

    yield _create_test_plan_templates

    created_test_plan_templates: List[TestPlanTemplateResponse] = []
    for response in responses:
        if response.created_test_plan_templates:
            created_test_plan_templates = (
                created_test_plan_templates + response.created_test_plan_templates
            )
        client.delete_test_plan_templates(
            ids=[
                test_plan_template.id
                for test_plan_template in created_test_plan_templates
            ]
        )


@pytest.mark.integration
@pytest.mark.enterprise
class TestPlanTemplateTest:

    def test__create_test_plan_template__returns_created_test_plan_template(
        self, client: TestPlanTemplateClient, create_test_plan_templates
    ):
        create_test_plan_template_request: List[TestPlanTemplateBase] = [
            TestPlanTemplateBase(
                name="Python integration test plan template",
                templateGroup="sample template group",
                workspace="33eba2fe-fe42-48a1-a47f-a6669479a8aa",
                executionActions=[ManualExecution(action="TEST", type="MANUAl")],
            )
        ]
        create_test_plan_template_response = create_test_plan_templates(
            create_test_plan_template_request
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
            == create_test_plan_template_request[0].name
        )

    def test__query_test_plan_template__returns_queried_test_plan_template(
        self, client: TestPlanTemplateClient, create_test_plan_templates
    ):

        create_test_plan_template_request: List[TestPlanTemplateBase] = [
            TestPlanTemplateBase(
                name="Python integration test plan template",
                templateGroup="sample template group",
                workspace="33eba2fe-fe42-48a1-a47f-a6669479a8aa",
                executionActions=[ManualExecution(action="TEST", type="MANUAl")],
            )
        ]

        create_test_plan_template_response = create_test_plan_templates(
            create_test_plan_template_request
        )

        template_id = (
            create_test_plan_template_response.created_test_plan_templates[0].id
            if create_test_plan_template_response.created_test_plan_templates
            and create_test_plan_template_response.created_test_plan_templates[0].id
            else None
        )

        assert template_id is not None

        query_test_plan_template_response: QueryTestPlanTemplatesResponse = (
            client.query_test_plan_templates(
                query_test_plan_templates=QueryTestPlanTemplatesRequest(
                    filter=f'id="{template_id}"', take=1
                )
            )
        )

        assert len(query_test_plan_template_response.test_plan_templates) == 1
        assert (
            query_test_plan_template_response.test_plan_templates[0].id == template_id
        )

    def test__delete_test_plan_template(self, client: TestPlanTemplateClient):

        create_test_plan_template_request: List[TestPlanTemplateBase] = [
            TestPlanTemplateBase(
                name="Python integration test plan template",
                templateGroup="sample template group",
                workspace="33eba2fe-fe42-48a1-a47f-a6669479a8aa",
                executionActions=[ManualExecution(action="TEST", type="MANUAl")],
            )
        ]
        create_test_plan_template_response: (
            CreateTestPlanTemplatePartialSuccessResponse
        ) = client.create_test_plan_templates(
            test_plan_templates=create_test_plan_template_request
        )

        template_id = (
            create_test_plan_template_response.created_test_plan_templates[0].id
            if create_test_plan_template_response.created_test_plan_templates
            and create_test_plan_template_response.created_test_plan_templates[0].id
            else None
        )

        assert template_id is not None

        client.delete_test_plan_templates(ids=[template_id])

        query_deleted_test_plan_template_response: QueryTestPlanTemplatesResponse = (
            client.query_test_plan_templates(
                query_test_plan_templates=QueryTestPlanTemplatesRequest(
                    filter=f'id="{template_id}"', take=1
                )
            )
        )

        assert len(query_deleted_test_plan_template_response.test_plan_templates) == 0

    def test_query_test_plan_templates_with_projections__returns_test_plan_templates_with_projected_properties(
        self, client: TestPlanTemplateClient
    ):
        query = QueryTestPlanTemplatesRequest(
            projection=[TestPlanTemplateField.ID, TestPlanTemplateField.NAME],
        )
        response = client.query_test_plan_templates(query_test_plan_templates=query)

        assert response is not None
        assert all(
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
            for test_plan_template in response.test_plan_templates
        )
