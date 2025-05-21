from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.test_plan import TestPlanClient
from nisystemlink.clients.test_plan.test_plan.models import (
    CreateTestPlanBodyContent,
    CreateTestPlansRequest,
    QueryTestPlansRequest,
    ScheduleTestPlanBodyContent,
    ScheduleTestPlansRequest,
    UpdateTestPlanBodyContent,
    UpdateTestPlansRequest,
)

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = TestPlanClient(configuration=server_configuration)

create_test_plans_request = CreateTestPlansRequest(
    testPlans=[
        CreateTestPlanBodyContent(
            name="Python integration test plan", state="NEW", partNumber="px40482"
        )
    ]
)

# create a test plan
created_test_plans = client.create_test_plans(create_request=create_test_plans_request)

created_test_plan_id = created_test_plans.createdTestPlans[0].id

# Query test plan using id.
query_test_plans_request = QueryTestPlansRequest(
    skip=0,
    take=1,
    descending=False,
    returnCount=False,
)
client.query_test_plans(query_request=query_test_plans_request)

# Get test plan
get_test_plan = client.get_test_plan(test_plan_id=created_test_plan_id)

# Update test plan
update_test_plans_request = UpdateTestPlansRequest(
    testPlans=[
        UpdateTestPlanBodyContent(
            id=created_test_plan_id,
            name="Updated Test Plan",
        )
    ]
)
updated_test_plan = client.update_test_plan(update_request=update_test_plans_request)

# Schedule the test plan
schedule_test_plans_request = ScheduleTestPlansRequest(
    test_plans=[
        ScheduleTestPlanBodyContent(
            id=created_test_plan_id,
            planned_start_date_time="2025-05-20T15:07:42.527Z",
            estimated_end_date_time="2025-05-20T15:07:42.527Z",
            system_id="fake-system",
        )
    ]
)
schedule_test_plan_response = client.schedule_test_plan(
    schedule_request=schedule_test_plans_request
)

# Delete test plan
client.delete_test_plans(ids=[created_test_plan_id])
