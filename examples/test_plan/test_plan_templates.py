from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan import TestPlanClient
from nisystemlink.clients.test_plan.models import (
    CreateTestPlanTemplateRequest,
    Dashboard,
    Job,
    JobExecution,
    ManualExecution,
    QueryTestPlanTemplatesRequest,
)


# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = TestPlanClient(configuration=server_configuration)

# Test plan template request metadata
create_test_plan_template_request = [
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
        file_ids=["file1", "file2"],
        # workspace="33eba2fe-fe42-48a1-a47f-a6669479a8aa",
        properties={"env": "staging", "priority": "high"},
        dashboard=Dashboard(
            id="DashBoardId", variables={"product": "PXIe-4080", "location": "Lab1"}
        ),
    )
]

# Create a test plan template
create_test_plan_template_response = client.create_test_plan_templates(
    test_plan_templates=create_test_plan_template_request
)

create_test_plan_template_id = None

if (
    create_test_plan_template_response.created_test_plan_templates
    and create_test_plan_template_response.created_test_plan_templates[0].id
):
    create_test_plan_template_id = str(
        create_test_plan_template_response.created_test_plan_templates[0].id
    )

# Query test plan templates using id
query_test_plan_template_request = QueryTestPlanTemplatesRequest(
    filter=f'id="{create_test_plan_template_id}"', take=1
)

client.query_test_plan_templates(
    query_test_plan_templates=query_test_plan_template_request
)

# Delete the created test plan template.
if create_test_plan_template_id is not None:
    client.delete_test_plan_templates(ids=[create_test_plan_template_id])
