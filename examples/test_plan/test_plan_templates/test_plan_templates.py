from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.test_plan.models._execution_definition import ManualExecution
from nisystemlink.clients.test_plan.test_plan_templates._test_plan_templates_client import TestPlanTemplateClient
from nisystemlink.clients.test_plan.test_plan_templates.models._query_test_plan_templates_request import QueryTestPlanTemplatesRequest
from nisystemlink.clients.test_plan.test_plan_templates.models._test_plan_templates import TestPlanTemplateBase

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = TestPlanTemplateClient(configuration=server_configuration)

#Test plan template request metadata
create_test_plan_template_request = [
        TestPlanTemplateBase(
            name = "Python integration test plan template",
            templateGroup = "sample template group",
            workspace = "33eba2fe-fe42-48a1-a47f-a6669479a8aa",
            executionActions=[
                ManualExecution(
                    action="TEST",
                    type="MANUAl"
                )
            ]
        )
    ]

# Create a test plan template
create_test_plan_template_response = client.create_test_plan_templates(test_plan_templates=create_test_plan_template_request)

create_test_plan_template_id = None

if create_test_plan_template_response.created_test_plan_templates and create_test_plan_template_response.created_test_plan_templates[0].id:
    create_test_plan_template_id = str(create_test_plan_template_response.created_test_plan_templates[0].id)

# Query test plan templates using id
query_test_plan_template_request = QueryTestPlanTemplatesRequest(
    filter=f'id="{create_test_plan_template_id}"',
    take=1
)

client.query_test_plan_templates(query_test_plan_templates=query_test_plan_template_request)

#Delete the created test plan template.
if create_test_plan_template_id is not None:
    client.delete_test_plan_templates(ids=[create_test_plan_template_id])