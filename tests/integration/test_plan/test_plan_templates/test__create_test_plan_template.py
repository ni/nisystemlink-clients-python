from typing import List
import pytest

from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.models._execution_definition import ManualExecutionDefinition
from nisystemlink.clients.test_plan.test_plan_templates._test_plan_templates_client import TestPlanTemplateClient
from nisystemlink.clients.test_plan.test_plan_templates.models._create_test_plan_templates import CreateTestPlanTemplateResponse
from nisystemlink.clients.test_plan.test_plan_templates.models._delete_test_plan_templates import DeleteTestPlanTemplates
from nisystemlink.clients.test_plan.test_plan_templates.models._query_test_plan_templates import QueryTestPlanTemplatesRequestBody, QueryTestPlanTemplatesResponse
from nisystemlink.clients.test_plan.test_plan_templates.models._test_plan_templates import TestPlanTemplateBase


@pytest.fixture(scope="class")
def create_test_plan_template() -> List[TestPlanTemplateBase]:
    """Fixture to create test plan template."""

    testPlanTemplates = [
        TestPlanTemplateBase(
            name = "Sample testplan template",
            templateGroup = "sample template group",
            workspace = "33eba2fe-fe42-48a1-a47f-a6669479a8aa",
            executionActions=[
                ManualExecutionDefinition(
                    action="TEST",
                    type="MANUAl"
                )
            ]
        )
    ]

    return testPlanTemplates

@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestPlanTemplateClient:
    """Fixture to create a TestPlanTemplateClient instance."""

    return TestPlanTemplateClient(enterprise_config)

@pytest.mark.integration
@pytest.mark.enterprise
class TestTestPlanTemplate:

    def test__create_test_plan_template__returns_created_test_plan_template(
            self, client: TestPlanTemplateClient, create_test_plan_template: List[TestPlanTemplateBase]
    ):
        create_test_plan_template_response: CreateTestPlanTemplateResponse = client.create_testPlanTemplates(
            testPlanTemplates=create_test_plan_template
        )

        template_id = (
            create_test_plan_template_response.createdTestPlanTemplates[0].id
            if create_test_plan_template_response.createdTestPlanTemplates and create_test_plan_template_response.createdTestPlanTemplates[0].id
            else None
        )

        assert template_id is not None

        client.delete_test_plan_templates(
            Ids=DeleteTestPlanTemplates(
                ids=[template_id]
            )
        )

        query_deleted_test_plan_template_response: QueryTestPlanTemplatesResponse = client.query_test_plan_templates(
            queryTestPlanTemplates=QueryTestPlanTemplatesRequestBody(
                filter=f'id="{template_id}"',
                take=1
            )
        )

        assert len(query_deleted_test_plan_template_response.testPlanTemplates) == 0

    def test__query_test_plan_template__returns_queried_test_plan_template(
            self, client: TestPlanTemplateClient, create_test_plan_template: List[TestPlanTemplateBase]
    ):
        create_test_plan_template_response: CreateTestPlanTemplateResponse = client.create_testPlanTemplates(
            testPlanTemplates=create_test_plan_template
        )

        template_id = (
            create_test_plan_template_response.createdTestPlanTemplates[0].id
            if create_test_plan_template_response.createdTestPlanTemplates and create_test_plan_template_response.createdTestPlanTemplates[0].id
            else None
        )

        assert template_id is not None

        query_test_plan_template_response: QueryTestPlanTemplatesResponse = client.query_test_plan_templates(
            queryTestPlanTemplates=QueryTestPlanTemplatesRequestBody(
                filter=f'id="{template_id}"',
                take=1
            )
        )

        assert len(query_test_plan_template_response.testPlanTemplates) == 1
        assert query_test_plan_template_response.testPlanTemplates[0].name == create_test_plan_template[0].name

        client.delete_test_plan_templates(
            Ids=DeleteTestPlanTemplates(
                ids=[template_id]
            )
        )

    def test__delete_test_plan_template(
            self, client: TestPlanTemplateClient, create_test_plan_template: List[TestPlanTemplateBase]
    ):
        create_test_plan_template_response: CreateTestPlanTemplateResponse = client.create_testPlanTemplates(
            testPlanTemplates=create_test_plan_template
        )

        template_id = (
            create_test_plan_template_response.createdTestPlanTemplates[0].id
            if create_test_plan_template_response.createdTestPlanTemplates and create_test_plan_template_response.createdTestPlanTemplates[0].id
            else None
        )

        assert template_id is not None

        client.delete_test_plan_templates(
            Ids=DeleteTestPlanTemplates(
                ids=[template_id]
            )
        )

        query_deleted_test_plan_template_response: QueryTestPlanTemplatesResponse = client.query_test_plan_templates(
            queryTestPlanTemplates=QueryTestPlanTemplatesRequestBody(
                filter=f'id="{template_id}"',
                take=1
            )
        )

        assert len(query_deleted_test_plan_template_response.testPlanTemplates) == 0
