

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.test_plans import TestPlansClient
from typing import List

@pytest.fixtures(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestPlansClient:
    """Fixture to create a TestPlansClient instance"""
    return TestPlansClient(enterprise_config)

@pytest.mark.integration
@pytest.mark.enterprise
class TestTestPlans:
    ...