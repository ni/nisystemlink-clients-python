import pytest
from typing import List

from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.test_plans import TestPlansClient
from nisystemlink.clients.test_plan.test_plans.models import (
    CreateTestPlanRequestBodyContent,
    CreateTestPlansRequest,
    CreateTestPlansResponse,
    TestPlan
)

@pytest.fixture(scope="class")
def test_plan_create() -> CreateTestPlansRequest:
    """Fixture to create create test plan object."""

    testPlan = CreateTestPlansRequest(
        testPlans=[
            CreateTestPlanRequestBodyContent(
                name="Sample Test Plan",
                state="NEW",
                partNumber="px40482"
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

    def test__get_test_plan__returns_get_test_plan(
        self, client: TestPlansClient
    ):
        get_test_plan_response: TestPlan = client.get_test_plan("1567158")

        assert get_test_plan_response is not None
        assert isinstance(get_test_plan_response, TestPlan)
        assert get_test_plan_response.id == "1567158"

    def test__create_test_plan__returns_created_test_plans(
        self, client: TestPlansClient, test_plan_create: CreateTestPlansRequest 
    ):
        test_plan_create_response: CreateTestPlansResponse = client.create_test_plans(
            testplans=test_plan_create
        )

        client.delete_test_plans(test_plan_ids=[test_plan_create_response.createdTestPlans[0].id])

        assert test_plan_create_response is not None
        assert len(test_plan_create_response.testPlans) == 1
        created_test_plan = test_plan_create_response.testPlans[0]
        assert created_test_plan.name == "Sample Test Plan"
        assert created_test_plan.state == "NEW"
        assert created_test_plan.partNumber == "px40482"
