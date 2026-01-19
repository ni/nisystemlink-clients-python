from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.notebook import NotebookClient
from nisystemlink.clients.notebook.models import (
    CreateExecutionRequest,
    ExecutionField,
    ExecutionPriority,
    ExecutionResourceProfile,
    ExecutionSortField,
    ExecutionStatus,
    QueryExecutionsRequest,
    ReportSettings,
    ReportType,
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = NotebookClient(configuration=server_configuration)


# Create a notebook execution
execution_request = CreateExecutionRequest(
    notebook_id="your_notebook_id",
    parameters={"param1": "value1"},
    workspace_id="your_workspace_id",
    timeout=300,
    result_cache_period=3600,
    report_settings=ReportSettings(
        format=ReportType.HTML,
        exclude_code=False,
    ),
    client_requests_id="your_client_request_id",
    priority=ExecutionPriority.HIGH,
    resource_profile=ExecutionResourceProfile.DEFAULT,
)

# Pass the list of execution requests to the create_executions method
create_execution_response = client.create_executions([execution_request])

# Get the execution by ID
execution = client.get_execution_by_id("your_execution_id")

# Query executions
query_request = QueryExecutionsRequest(
    filter=f"(status = {ExecutionStatus.FAILED.value}))",
    order_by=ExecutionSortField.COMPLETED_AT,
    descending=True,
    projection=[
        ExecutionField.ID,
        ExecutionField.NOTEBOOK_ID,
        ExecutionField.STATUS,
    ],
)

query_executions_response = client.query_executions(query_request)

# Cancel execution
cancel_execution_response = client.cancel_executions(["your_execution_id"])

# Retry execution
retry_execution_response = client.retry_executions(["your_execution_id"])

# Create execution from existing one
run_new = client.create_executions_from_existing(["your_execution_id"])
