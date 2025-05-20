from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.test_plan.test_plan_templates.models._test_plan_templates import (
    TestPlanTemplateResponse,
)


class QueryTestPlanTemplatesResponse(JsonModel):
    """Response information for the query test plan templates API."""

    test_plan_templates: List[TestPlanTemplateResponse]
    """Queried test plan templates."""

    continuation_token: Optional[str] = None
    """Allows users to continue the query at the next test plan templates that matches the given criteria.

    To retrieve the next page of test plan templates, pass the continuation token from the previous
    page in the next request. The service responds with the next page of data and provides a new
    continuation token. To paginate results, continue sending requests with the newest continuation
    token provided in each response."""
