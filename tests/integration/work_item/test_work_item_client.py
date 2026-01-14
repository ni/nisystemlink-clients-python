import copy
from datetime import datetime
from typing import List

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.work_item import WorkItemClient
from nisystemlink.clients.work_item.models import (
    CreateWorkItemRequest,
    CreateWorkItemsPartialSuccessResponse,
    CreateWorkItemTemplateRequest,
    CreateWorkItemTemplatesPartialSuccessResponse,
    Dashboard,
    ExecutionDefinition,
    Job,
    JobExecution,
    ManualExecution,
    QueryWorkItemsRequest,
    QueryWorkItemTemplatesRequest,
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
    TemplateResourceDefinition,
    TemplateResourcesDefinition,
    TemplateTimelineDefinition,
    TimelineDefinition,
    UpdateWorkItemRequest,
    UpdateWorkItemsRequest,
    UpdateWorkItemTemplateRequest,
    UpdateWorkItemTemplatesRequest,
    WorkItem,
    WorkItemField,
    WorkItemTemplate,
    WorkItemTemplateField,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> WorkItemClient:
    """Fixture to create a WorkItemClient instance"""
    return WorkItemClient(enterprise_config)


@pytest.fixture
def create_work_items(client: WorkItemClient):
    """Fixture to return a factory that creates work items."""
    responses: List[CreateWorkItemsPartialSuccessResponse] = []

    def _create_work_items(
        new_work_items: List[CreateWorkItemRequest],
    ) -> CreateWorkItemsPartialSuccessResponse:
        response = client.create_work_items(work_items=new_work_items)
        responses.append(response)
        return response

    yield _create_work_items

    created_work_items: List[WorkItem] = []
    for response in responses:
        if response.created_work_items:
            created_work_items += response.created_work_items

    client.delete_work_items(
        work_item_ids=[
            work_item.id for work_item in created_work_items if work_item.id is not None
        ]
    )


@pytest.fixture
def create_work_item_templates(client: WorkItemClient):
    """Fixture to return a factory that creates work item templates."""
    responses: List[CreateWorkItemTemplatesPartialSuccessResponse] = []

    def _create_work_item_templates(
        new_work_item_templates: List[CreateWorkItemTemplateRequest],
    ) -> CreateWorkItemTemplatesPartialSuccessResponse:
        response = client.create_work_item_templates(
            work_item_templates=new_work_item_templates
        )
        responses.append(response)
        return response

    yield _create_work_item_templates

    created_work_item_templates: List[WorkItemTemplate] = []
    for response in responses:
        if response.created_work_item_templates:
            created_work_item_templates += response.created_work_item_templates

    client.delete_work_item_templates(
        work_item_template_ids=[
            work_item_template.id
            for work_item_template in created_work_item_templates
            if work_item_template.id is not None
        ]
    )


@pytest.mark.integration
@pytest.mark.enterprise
class TestWorkItemClient:

    _workspace = "2300760d-38c4-48a1-9acb-800260812337"
    """Used the main-test default workspace since the client
    for creating a workspace has not been added yet"""

    _dashboard = Dashboard(
        id="DashBoardId", variables={"product": "PXIe-4080", "location": "Lab1"}
    )

    _execution_actions: List[ExecutionDefinition] = [
        ManualExecution(action="START", type="MANUAL"),
        JobExecution(
            action="ABORT",
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
    ]

    _create_work_item_request = [
        CreateWorkItemRequest(
            name="Python integration work item",
            type="testplan",
            state="NEW",
            description="Work item for verifying integration flow",
            assigned_to="test.user@example.com",
            requested_by="test.manager@example.com",
            test_program="TP-Integration-001",
            part_number="px40482",
            workspace=_workspace,
            timeline=TimelineDefinition(
                earliest_start_date_time=datetime(2026, 1, 15, 8, 0, 0),
                due_date_time=datetime(2026, 1, 20, 17, 0, 0),
                estimated_duration_in_seconds=3600,
            ),
            resources=ResourcesDefinition(
                assets=ResourceDefinition(
                    selections=[
                        ResourceSelectionDefinition(
                            id="asset-001",
                            target_location_id="loc-001",
                            target_system_id="sys-001",
                            target_parent_id=None,
                        )
                    ],
                    filter="modelName = 'cRIO-9045' AND serialNumber = '01E82ED0'",
                ),
                duts=ResourceDefinition(
                    selections=[
                        ResourceSelectionDefinition(
                            id="dut-001",
                            target_location_id="loc-002",
                            target_system_id="sys-002",
                            target_parent_id=None,
                        )
                    ],
                    filter="modelName = 'cRIO-9045' AND serialNumber = '01E82ED0'",
                ),
                fixtures=ResourceDefinition(
                    selections=[
                        ResourceSelectionDefinition(
                            id="fixture-001",
                            target_location_id="loc-003",
                            target_system_id="sys-003",
                            target_parent_id=None,
                        )
                    ],
                    filter="modelName = 'cRIO-9045' AND serialNumber = '01E82ED0'",
                ),
                systems=SystemResourceDefinition(
                    selections=[
                        SystemResourceSelectionDefinition(
                            id="system-001",
                            target_location_id="loc-004",
                        )
                    ],
                    filter="os:linux AND arch:x64",
                ),
            ),
            file_ids_from_template=["file1", "file2"],
            properties={"env": "staging", "priority": "high"},
            dashboard=_dashboard,
            execution_actions=_execution_actions,
        )
    ]
    """create work item request object."""

    _create_work_item_template_request = [
        CreateWorkItemTemplateRequest(
            name="Python integration work item template",
            template_group="sample template group",
            type="testplan",
            product_families=["FamilyA", "FamilyB"],
            part_numbers=["PN-1001", "PN-1002"],
            summary="Template for running integration work items",
            description="This template defines execution steps for integration workflows.",
            test_program="TP-INT-002",
            timeline=TemplateTimelineDefinition(
                estimated_duration_in_seconds=3600,
            ),
            resources=TemplateResourcesDefinition(
                assets=TemplateResourceDefinition(
                    filter="modelName = 'cRIO-9045' AND serialNumber = '01E82ED0'"
                ),
                duts=TemplateResourceDefinition(
                    filter="modelName = 'cRIO-9045' AND serialNumber = '01E82ED0'"
                ),
                fixtures=TemplateResourceDefinition(
                    filter="modelName = 'cRIO-9045' AND serialNumber = '01E82ED0'"
                ),
                systems=TemplateResourceDefinition(filter="os:linux AND arch:x64"),
            ),
            execution_actions=_execution_actions,
            file_ids=["file1", "file2"],
            workspace=_workspace,
            properties={"env": "staging", "priority": "high"},
            dashboard=_dashboard,
        )
    ]
    """create work item template request object."""

    def test__create_work_item__returns_created_work_items(
        self, client: WorkItemClient, create_work_items
    ):
        create_work_item_template_response = client.create_work_item_templates(
            work_item_templates=self._create_work_item_template_request
        )
        template_id = (
            create_work_item_template_response.created_work_item_templates[0].id
            if create_work_item_template_response.created_work_item_templates
            and create_work_item_template_response.created_work_item_templates[0].id
            else None
        )
        assert template_id is not None
        work_item_request = copy.deepcopy(self._create_work_item_request)
        work_item_request[0].template_id = template_id

        create_work_item_response = create_work_items(work_item_request)

        assert create_work_item_response.created_work_items is not None
        created_work_item = create_work_item_response.created_work_items[0]
        assert created_work_item is not None
        assert created_work_item.name == "Python integration work item"
        assert created_work_item.type == "testplan"
        assert created_work_item.part_number == "px40482"
        delete_work_item_template_response = client.delete_work_item_templates(
            work_item_template_ids=[template_id]
        )
        assert delete_work_item_template_response is None

    def test__get_work_item__returns_work_item(
        self, client: WorkItemClient, create_work_items
    ):
        create_work_item_response = create_work_items(self._create_work_item_request)
        assert create_work_item_response.created_work_items is not None
        created_work_item_id = create_work_item_response.created_work_items[0].id

        get_work_item_response = client.get_work_item(work_item_id=created_work_item_id)

        assert get_work_item_response is not None
        assert isinstance(get_work_item_response, WorkItem)
        assert get_work_item_response.id == created_work_item_id

    def test__update_work_item__returns_updated_work_item(
        self, client: WorkItemClient, create_work_items
    ):
        create_work_item_response = create_work_items(self._create_work_item_request)
        assert create_work_item_response.created_work_items is not None
        created_work_item = create_work_item_response.created_work_items[0]

        update_work_items_request = UpdateWorkItemsRequest(
            work_items=[
                UpdateWorkItemRequest(
                    id=created_work_item.id,
                    name="Updated Work Item",
                )
            ]
        )
        update_work_items_response = client.update_work_items(
            update_work_items=update_work_items_request
        )

        assert update_work_items_response.updated_work_items is not None
        updated_work_item = update_work_items_response.updated_work_items[0]
        assert updated_work_item.id == created_work_item.id
        assert updated_work_item.name == "Updated Work Item"

    def test__schedule_work_item__returns_scheduled_work_item(
        self, client: WorkItemClient, create_work_items
    ):
        create_work_item_response = create_work_items(self._create_work_item_request)
        assert create_work_item_response.created_work_items is not None
        created_work_item = create_work_item_response.created_work_items[0]

        schedule_work_items_request = ScheduleWorkItemsRequest(
            work_items=[
                ScheduleWorkItemRequest(
                    id=created_work_item.id,
                    schedule=ScheduleDefinition(
                        planned_start_date_time=datetime.strptime(
                            "2025-05-20T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        planned_end_date_time=datetime.strptime(
                            "2025-05-22T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                    ),
                    resources=ScheduleResourcesDefinition(
                        systems=ScheduleSystemResourceDefinition(
                            selections=[
                                SystemResourceSelectionDefinition(id="fake-system")
                            ]
                        ),
                    ),
                )
            ],
            replace=True,
        )
        schedule_work_items_response = client.schedule_work_items(
            schedule_work_items=schedule_work_items_request
        )

        assert schedule_work_items_response.scheduled_work_items is not None
        scheduled_work_item = schedule_work_items_response.scheduled_work_items[0]
        assert scheduled_work_item.id == created_work_item.id
        assert scheduled_work_item.schedule is not None
        assert (
            scheduled_work_item.schedule.planned_start_date_time
            == datetime.strptime("2025-05-20T15:07:42.527Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        assert scheduled_work_item.resources is not None
        assert scheduled_work_item.resources.systems is not None
        assert scheduled_work_item.resources.systems.selections is not None
        assert scheduled_work_item.resources.systems.selections[0].id == "fake-system"

    def test__query_work_items__return_queried_work_item(
        self, client: WorkItemClient, create_work_items
    ):
        create_work_item_response = create_work_items(self._create_work_item_request)
        assert create_work_item_response.created_work_items is not None
        created_work_item = create_work_item_response.created_work_items[0]

        query_work_items_request = QueryWorkItemsRequest(
            filter=f'id = "{created_work_item.id}"', return_count=True
        )
        queried_work_items_response = client.query_work_items(
            query_work_items=query_work_items_request
        )

        assert queried_work_items_response is not None
        assert queried_work_items_response.work_items[0].id == created_work_item.id
        assert queried_work_items_response.total_count is not None
        assert queried_work_items_response.total_count > 0

    def test__query_work_items_with_projections__returns_the_work_items_with_projected_properties(
        self, client: WorkItemClient, create_work_items
    ):
        create_work_item_response = create_work_items(self._create_work_item_request)
        assert create_work_item_response.created_work_items is not None
        created_work_item = create_work_item_response.created_work_items[0]

        query_work_items_request = QueryWorkItemsRequest(
            filter=f'id = "{created_work_item.id}"',
            projection=[WorkItemField.ID, WorkItemField.NAME],
            take=1,
        )
        response = client.query_work_items(query_work_items=query_work_items_request)

        assert response is not None
        work_item = response.work_items[0]
        assert (
            work_item.id is not None
            and work_item.name is not None
            and work_item.template_id is None
            and work_item.state is None
            and work_item.description is None
            and work_item.parent_id is None
            and work_item.assigned_to is None
            and work_item.requested_by is None
            and work_item.workspace is None
            and work_item.created_by is None
            and work_item.updated_at is None
            and work_item.created_at is None
            and work_item.updated_by is None
            and work_item.properties is None
            and work_item.part_number is None
            and work_item.test_program is None
            and work_item.timeline is None
            and work_item.resources is None
            and work_item.file_ids_from_template is None
            and work_item.execution_actions is None
            and work_item.execution_history is None
            and work_item.dashboard is None
        )

    def test__delete_work_item(self, client: WorkItemClient, create_work_items):
        create_work_item_response = create_work_items(self._create_work_item_request)
        assert create_work_item_response.created_work_items is not None
        created_work_item = create_work_item_response.created_work_items[0]

        client.delete_work_items(work_item_ids=[created_work_item.id])

        query_deleted_work_item_response = client.query_work_items(
            query_work_items=QueryWorkItemsRequest(
                filter=f'id="{created_work_item.id}"', take=1
            )
        )
        assert len(query_deleted_work_item_response.work_items) == 0

    def test__create_work_item_template__returns_created_work_item_template(
        self, create_work_item_templates
    ):
        create_work_item_template_response = create_work_item_templates(
            self._create_work_item_template_request
        )

        assert (
            create_work_item_template_response.created_work_item_templates is not None
        )
        created_work_item_template = (
            create_work_item_template_response.created_work_item_templates[0]
        )
        assert created_work_item_template is not None
        assert (
            created_work_item_template.name == "Python integration work item template"
        )
        assert created_work_item_template.type == "testplan"

    def test__update_work_item_template__returns_updated_work_item_template(
        self, client: WorkItemClient, create_work_item_templates
    ):
        create_work_item_template_response = create_work_item_templates(
            self._create_work_item_template_request
        )
        assert (
            create_work_item_template_response.created_work_item_templates is not None
        )
        created_work_item_template = (
            create_work_item_template_response.created_work_item_templates[0]
        )

        update_work_item_templates_request = UpdateWorkItemTemplatesRequest(
            work_item_templates=[
                UpdateWorkItemTemplateRequest(
                    id=created_work_item_template.id,
                    name="Updated Work Item Template",
                )
            ]
        )
        update_work_item_templates_response = client.update_work_item_templates(
            update_work_item_templates=update_work_item_templates_request
        )

        assert (
            update_work_item_templates_response.updated_work_item_templates is not None
        )
        updated_work_item_template = (
            update_work_item_templates_response.updated_work_item_templates[0]
        )
        assert updated_work_item_template.id == created_work_item_template.id
        assert updated_work_item_template.name == "Updated Work Item Template"

    def test__query_work_item_template__returns_queried_work_item_template(
        self, client: WorkItemClient, create_work_item_templates
    ):
        create_work_item_template_response = create_work_item_templates(
            self._create_work_item_template_request
        )
        assert (
            create_work_item_template_response.created_work_item_templates is not None
        )
        created_work_item_template = (
            create_work_item_template_response.created_work_item_templates[0]
        )
        assert created_work_item_template is not None

        query = QueryWorkItemTemplatesRequest(
            filter=f'id="{created_work_item_template.id}"', take=1
        )
        query_work_item_template_response = client.query_work_item_templates(
            query_work_item_templates=query
        )

        assert query_work_item_template_response is not None
        assert len(query_work_item_template_response.work_item_templates) == 1
        assert (
            query_work_item_template_response.work_item_templates[0].id
            == created_work_item_template.id
        )

    def test__query_work_item_templates_with_projections__returns_work_item_templates_with_projected_properties(
        self, client: WorkItemClient, create_work_item_templates
    ):
        create_work_item_template_response = create_work_item_templates(
            self._create_work_item_template_request
        )
        assert (
            create_work_item_template_response.created_work_item_templates is not None
        )
        created_work_item_template = (
            create_work_item_template_response.created_work_item_templates[0]
        )
        assert created_work_item_template is not None

        query = QueryWorkItemTemplatesRequest(
            filter=f'id="{created_work_item_template.id}"',
            projection=[WorkItemTemplateField.ID, WorkItemTemplateField.NAME],
            take=1,
        )
        response = client.query_work_item_templates(query_work_item_templates=query)

        assert response is not None
        work_item_template = response.work_item_templates[0]
        assert (
            work_item_template.id is not None
            and work_item_template.name is not None
            and work_item_template.template_group is None
            and work_item_template.type is None
            and work_item_template.product_families is None
            and work_item_template.part_numbers is None
            and work_item_template.summary is None
            and work_item_template.description is None
            and work_item_template.test_program is None
            and work_item_template.timeline is None
            and work_item_template.resources is None
            and work_item_template.execution_actions is None
            and work_item_template.file_ids is None
            and work_item_template.workspace is None
            and work_item_template.properties is None
            and work_item_template.dashboard is None
        )

    def test__delete_work_item_template(
        self, client: WorkItemClient, create_work_item_templates
    ):
        create_work_item_template_response = create_work_item_templates(
            self._create_work_item_template_request
        )
        assert (
            create_work_item_template_response.created_work_item_templates is not None
        )
        created_work_item_template = (
            create_work_item_template_response.created_work_item_templates[0]
        )

        client.delete_work_item_templates(
            work_item_template_ids=[created_work_item_template.id]
        )

        query_deleted_work_item_template_response = client.query_work_item_templates(
            query_work_item_templates=QueryWorkItemTemplatesRequest(
                filter=f'id="{created_work_item_template.id}"', take=1
            )
        )
        assert len(query_deleted_work_item_template_response.work_item_templates) == 0
