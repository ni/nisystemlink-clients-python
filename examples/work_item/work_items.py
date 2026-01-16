from datetime import datetime

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.work_item import WorkItemClient
from nisystemlink.clients.work_item.models import (
    CreateWorkItemRequest,
    Dashboard,
    Job,
    JobExecution,
    ManualExecution,
    QueryWorkItemsRequest,
    ResourceDefinition,
    ResourcesDefinition,
    ResourceSelectionDefinition,
    ScheduleDefinition,
    ScheduleResourcesDefinition,
    ScheduleSystemResourceDefinition,
    ScheduleWorkItemRequest,
    ScheduleWorkItemsRequest,
    SystemResourceDefinition,
    SystemResourceSelectionDefinition,
    TimelineDefinition,
    UpdateWorkItemRequest,
    UpdateWorkItemsRequest,
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

create_work_items_request = [
    CreateWorkItemRequest(
        name="Python integration work item",
        type="testplan",
        state="NEW",
        description="Work item for verifying integration flow",
        assigned_to="test.user@example.com",
        requested_by="test.manager@example.com",
        properties={"env": "staging", "priority": "high"},
        part_number="px40482",
        test_program="TP-Integration-001",
        workspace="your_workspace_id",
        timeline=TimelineDefinition(
            earliest_start_date_time=datetime.strptime(
                "2024-01-15T08:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
            ),
            due_date_time=datetime.strptime(
                "2024-01-20T17:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
            ),
            estimated_duration_in_seconds=86400,
        ),
        resources=ResourcesDefinition(
            systems=SystemResourceDefinition(
                selections=[
                    SystemResourceSelectionDefinition(
                        id="system-001",
                        target_location_id="location-001",
                    ),
                ],
                filter='properties.data["Lab"] = "Battery Pack Lab"',
            ),
            duts=ResourceDefinition(
                selections=[
                    ResourceSelectionDefinition(
                        id="dut-001",
                        target_location_id="location-001",
                        target_system_id="system-001",
                        target_parent_id="parent-001",
                    ),
                ],
                filter='modelName = "cRIO-9045" && serialNumber = "01E82ED0"',
            ),
            assets=ResourceDefinition(
                selections=[
                    ResourceSelectionDefinition(
                        id="asset-001",
                        target_location_id="location-001",
                        target_system_id="system-001",
                        target_parent_id="parent-001",
                    ),
                ],
                filter='modelName = "cRIO-9045" && serialNumber = "01E82ED0"',
            ),
            fixtures=ResourceDefinition(
                selections=[
                    ResourceSelectionDefinition(
                        id="fixture-001",
                        target_location_id="location-001",
                        target_system_id="system-001",
                        target_parent_id="parent-001",
                    ),
                ],
                filter='modelName = "cRIO-9045" && serialNumber = "01E82ED0"',
            ),
        ),
        file_ids_from_template=["file1", "file2"],
        dashboard=Dashboard(
            id="DashboardId", variables={"product": "PXIe-4080", "location": "Lab1"}
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

# create work item
create_work_items_response = client.create_work_items(
    work_items=create_work_items_request
)

if create_work_items_response.created_work_items:
    created_work_item_id = create_work_items_response.created_work_items[0].id
    print(f"Created work item: {created_work_item_id}")

# Query work items using id.
query_work_items_request = QueryWorkItemsRequest(
    filter=f'id = "{created_work_item_id}"',
    take=1,
    descending=False,
    return_count=False,
)
query_work_items_response = client.query_work_items(
    query_work_items=query_work_items_request
)
if query_work_items_response.work_items:
    print(f"Found work item: {query_work_items_response.work_items[0].name}")

# Get work item
if created_work_item_id is not None:
    get_work_item_response = client.get_work_item(work_item_id=created_work_item_id)
    print(f"Retrieved work item: {get_work_item_response.name}")

# Update work item
if created_work_item_id is not None:
    update_work_items_request = UpdateWorkItemsRequest(
        work_items=[
            UpdateWorkItemRequest(id=created_work_item_id, name="Updated work item")
        ]
    )
    update_work_items_response = client.update_work_items(
        update_work_items=update_work_items_request
    )
    if update_work_items_response.updated_work_items:
        print(
            f"Work item name updated to: {update_work_items_response.updated_work_items[0].name}"
        )

# Schedule work item
if created_work_item_id is not None:
    schedule_work_items_request = ScheduleWorkItemsRequest(
        work_items=[
            ScheduleWorkItemRequest(
                id=created_work_item_id,
                schedule=ScheduleDefinition(
                    planned_start_date_time=datetime.strptime(
                        "2025-05-20T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    planned_end_date_time=datetime.strptime(
                        "2025-05-22T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    planned_duration_in_seconds=172800,
                ),
                resources=ScheduleResourcesDefinition(
                    systems=ScheduleSystemResourceDefinition(
                        selections=[
                            SystemResourceSelectionDefinition(
                                id="system-123",
                                target_location_id="location-456",
                            )
                        ]
                    )
                ),
            )
        ],
        replace=True,
    )
    schedule_work_items_response = client.schedule_work_items(
        schedule_work_items=schedule_work_items_request
    )
    if schedule_work_items_response.scheduled_work_items:
        print(
            f"Scheduled work item with ID: {schedule_work_items_response.scheduled_work_items[0].id}"
        )

# Delete work item
if created_work_item_id is not None:
    client.delete_work_items(ids=[created_work_item_id])
    print("Work item deleted successfully.")
