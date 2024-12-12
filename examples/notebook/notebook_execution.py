from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.notebook import NotebookClient
from nisystemlink.clients.notebook.models import (
    CreateExecutionRequest,
    Source,
    SourceType,
    ReportSettings,
    ReportType,
    ExecutionPriority,
    ExecutionResourceProfile,
    QueryExecutionsRequest,
    ExecutionStatus,
    ExecutionSortField,
    ExecutionField,
)

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = NotebookClient(configuration=server_configuration)


# Create a notebook execution
execution_request = CreateExecutionRequest(
    notebook_id="your_notebook_id",
    parameters={"param1": "value1"},
    workspace_id="your_workspace_id",
    timeout=300,
    result_cache_period=3600,
    source=Source(
        type=SourceType.MANUAL,
        routine_service="your_routine_service",
        routine_name="your_routine_name",
    ),
    report_settings=ReportSettings(
        format=ReportType.HTML,
        exclude_code=False,
    ),
    client_requests_id="your_client_request_id",
    priority=ExecutionPriority.NORMAL,
    resource_profile=ExecutionResourceProfile.DEFAULT,
)

# Pass the list of execution requests to the create_executions method
response = client.create_executions([execution_request])

# Get the execution by ID
execution = client.get_execution_by_id("your_execution_id")

# Query executions
query_request = QueryExecutionsRequest(
    filter=f'(status = {ExecutionStatus.FAILED.value} && DateTime(completedAt) > DateTime.parse(\\"2023-04-10T07:22:40.339Z\\"))',
    order_by=ExecutionSortField.COMPLETED_AT,
    descending=True,
    projection=[
        ExecutionField.ID,
        ExecutionField.NOTEBOOK_ID,
        ExecutionField.STATUS,
        "reportSettings.format",
    ],
)
