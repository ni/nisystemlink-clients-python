from datetime import datetime

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.test_plan import TestPlanClient
from nisystemlink.clients.test_plan.models import (
    CreateTestPlanRequest,
    Dashboard,
    Job,
    JobExecution,
    ManualExecution,
    QueryTestPlansRequest,
    ScheduleTestPlanRequest,
    ScheduleTestPlansRequest,
    UpdateTestPlanRequest,
    UpdateTestPlansRequest,
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = TestPlanClient(configuration=server_configuration)

create_test_plans_request = [
    CreateTestPlanRequest(
        name="Python integration test plan",
        state="NEW",
        description="Test plan for verifying integration flow",
        assigned_to="test.user@example.com",
        estimated_duration_in_seconds=86400,
        properties={"env": "staging", "priority": "high"},
        part_number="px40482",
        dut_id="Sample-Dut_Id",
        dut_serial_number="serial_number_123",
        test_program="TP-Integration-001",
        system_filter="os:linux AND arch:x64",
        dut_filter="modelName = 'cRIO-9045' AND serialNumber = '01E82ED0'",
        workspace="your_workspace_id",
        file_ids_from_template=["file1", "file2"],
        dashboard=Dashboard(
            id="DashBoardId", variables={"product": "PXIe-4080", "location": "Lab1"}
        ),
        execution_actions=[
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
        ],
    )
]

# create a test plan
created_test_plans_response = client.create_test_plans(
    test_plans=create_test_plans_request
)

if created_test_plans_response.created_test_plans:
    created_test_plan_id = created_test_plans_response.created_test_plans[0].id

# Query test plan using id.
query_test_plans_request = QueryTestPlansRequest(
    take=1, descending=False, return_count=False
)
client.query_test_plans(query_request=query_test_plans_request)

# Get test plan
get_test_plan = client.get_test_plan(test_plan_id=created_test_plan_id)

# Update test plan
update_test_plans_request = UpdateTestPlansRequest(
    test_plans=[
        UpdateTestPlanRequest(
            id=created_test_plan_id,
            name="Updated Test Plan",
        )
    ]
)
updated_test_plan = client.update_test_plans(update_request=update_test_plans_request)

# Schedule the test plan
schedule_test_plans_request = ScheduleTestPlansRequest(
    test_plans=[
        ScheduleTestPlanRequest(
            id=created_test_plan_id,
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
schedule_test_plan_response = client.schedule_test_plans(
    schedule_request=schedule_test_plans_request
)

# Delete test plan
client.delete_test_plans(ids=[created_test_plan_id])
