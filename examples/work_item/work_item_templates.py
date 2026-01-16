from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.work_item import WorkItemClient
from nisystemlink.clients.work_item.models import (
    CreateWorkItemTemplateRequest,
    Dashboard,
    Job,
    JobExecution,
    ManualExecution,
    QueryWorkItemTemplatesRequest,
    TemplateResourceDefinition,
    TemplateResourcesDefinition,
    TemplateTimelineDefinition,
    UpdateWorkItemTemplateRequest,
    UpdateWorkItemTemplatesRequest,
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = WorkItemClient(configuration=server_configuration)

create_work_item_template_request = [
    CreateWorkItemTemplateRequest(
        name="Python integration work item template",
        template_group="sample template group",
        type="testplan",
        product_families=["FamilyA", "FamilyB"],
        part_numbers=["PN-1001", "PN-1002"],
        summary="Template for running integration work items",
        description="This template defines execution steps for integration workflows.",
        test_program="TP-INT-002",
        timeline=TemplateTimelineDefinition(estimated_duration_in_seconds=86400),
        resources=TemplateResourcesDefinition(
            systems=TemplateResourceDefinition(
                filter='properties.data["Lab"] = "Battery Pack Lab" && state = "Available"'
            ),
            duts=TemplateResourceDefinition(
                filter='modelName = "cRIO-9045" && serialNumber = "01E82ED0"'
            ),
            assets=TemplateResourceDefinition(
                filter='modelName = "cRIO-9045" && serialNumber = "01E82ED0"'
            ),
            fixtures=TemplateResourceDefinition(
                filter='modelName = "cRIO-9045" && serialNumber = "01E82ED0"'
            ),
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
        file_ids=["file1", "file2"],
        workspace="your_workspace_id",
        properties={"env": "staging", "priority": "high"},
        dashboard=Dashboard(
            id="DashboardId", variables={"product": "PXIe-4080", "location": "Lab1"}
        ),
    )
]

# Create work item template
create_work_item_templates_response = client.create_work_item_templates(
    work_item_templates=create_work_item_template_request
)

if create_work_item_templates_response.created_work_item_templates:
    create_work_item_template_id = (
        create_work_item_templates_response.created_work_item_templates[0].id
    )
    print(f"Created work item template: {create_work_item_template_id}")

# Query work item templates using id
query_work_item_template_request = QueryWorkItemTemplatesRequest(
    filter=f'id="{create_work_item_template_id}"', take=1
)
query_work_item_templates_response = client.query_work_item_templates(
    query_work_item_templates=query_work_item_template_request
)
if query_work_item_templates_response.work_item_templates:
    print(
        f"Found work item template: {query_work_item_templates_response.work_item_templates[0].name}"
    )

# Update work item template
if create_work_item_template_id is not None:
    update_work_item_template_request = UpdateWorkItemTemplatesRequest(
        work_item_templates=[
            UpdateWorkItemTemplateRequest(
                id=create_work_item_template_id, name="Updated work item template"
            )
        ]
    )
    update_work_item_templates_response = client.update_work_item_templates(
        update_work_item_templates=update_work_item_template_request
    )
    if update_work_item_templates_response.updated_work_item_templates:
        print(
            "Work item template name updated to: "
            f"{update_work_item_templates_response.updated_work_item_templates[0].name}"
        )

# Delete work item template
if create_work_item_template_id is not None:
    client.delete_work_item_templates(ids=[create_work_item_template_id])
    print("Work item template deleted successfully.")
