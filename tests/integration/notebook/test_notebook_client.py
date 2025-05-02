import logging
import string
from random import choices
import typing

import pytest
import responses
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.notebook import NotebookClient
from nisystemlink.clients.notebook.models import (
    CreateExecutionRequest,
    ExecutionField,
    ExecutionSortField,
    ExecutionStatus,
    NotebookMetadata,
    QueryExecutionsRequest,
    QueryNotebookRequest,
)

TEST_FILE_DATA = b"This is a test notebook binary content."
PREFIX = "Notebook Client Tests-"
BASE_URL = "https://test-api.lifecyclesolutions.ni.com"


@pytest.fixture(scope="class")
def client(enterprise_config) -> NotebookClient:
    """Fixture to create a NotebookClient instance."""
    return NotebookClient(enterprise_config)


@pytest.fixture()
def random_filename() -> str:
    """Generate a random filename for each test in test class."""
    rand_file_name = "".join(choices(string.ascii_letters + string.digits, k=10))

    name = f"{PREFIX}{rand_file_name}.ipynb"
    logging.info(f"Random filename: {name}")
    return name


@pytest.fixture()
def create_notebook(client: NotebookClient):
    """Fixture to return a factory that creates a notebook."""
    notebook_ids = []

    def _create_notebook(
        metadata: NotebookMetadata, cleanup: bool = True
    ) -> NotebookMetadata:

        # file_bytes = file.read()  # Read file as bytes
        with open("tests/integration/notebook/sample_file.ipynb", "rb") as file:
            try:
                notebook_response = client.create_notebook(metadata=metadata, content=file)
            except ApiException as e:
                logging.warning(f"Error creating notebook: {metadata.json(by_alias=True, exclude_unset=True)}")
                raise
        if cleanup:
            notebook_ids.append(notebook_response.id)

        return notebook_response

    yield _create_notebook

    if notebook_ids:
        for notebook_id in filter(None, notebook_ids):
            client.delete_notebook(id=notebook_id)


@pytest.fixture()
def update_notebook(client: NotebookClient):
    """Fixture to return a factory that updates a notebook."""
    def _update_notebook(
        id: str,
        metadata: NotebookMetadata = None,
        content: typing.BinaryIO = None,
    ) -> NotebookMetadata:

        try:
            notebook_response = client.update_notebook(id=id, metadata=metadata, content=content)
        except ApiException as e:
            if (metadata is not None):
                logging.warning(f"Error updating notebook {id}: {metadata.json(by_alias=True, exclude_unset=True)}")
            raise

        return notebook_response

    return _update_notebook


@pytest.mark.enterprise
@pytest.mark.integration
class TestNotebookClient:
    def test__create_notebook_with_valid_file_and_metadata__notebook_created_with_valid_metadata(
        self, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        assert notebook.name == random_filename
        assert notebook.workspace is not None
        assert notebook.created_by is not None
        assert notebook.created_at is not None

    def test__create_notebook_with_invalid_file__raises_ApiException_BadRequest(
        self, client, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        with pytest.raises(ApiException, match="Bad Request"):
            with open(
                "tests/integration/notebook/test_notebook_client.py", "rb"
            ) as file:
                client.create_notebook(metadata=metadata, content=file)

    def test__create_notebook_with_duplicate_file_name__raises_ApiException_BadRequest(
        self, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        create_notebook(metadata=metadata)

        with pytest.raises(ApiException, match="409 Conflict"):
            create_notebook(metadata=metadata)

    def test__create_notebook_with_invalid_workspace__raises_ApiException_BadRequest(
        self, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename, workspace="invalid_workspace")
        with pytest.raises(ApiException, match="Bad Request"):
            create_notebook(metadata=metadata)

    def test__get_notebook_with_valid_id__returns_notebook_with_right_field_values(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        response = client.get_notebook(id=notebook.id)

        assert response.id == notebook.id
        assert response.workspace is not None
        assert response.created_by is not None
        assert response.created_at is not None
        assert response.name == notebook.name == random_filename

    def test__get_notebook_with_invalid_id__raises_ApiException_NotFound(self, client):
        with pytest.raises(ApiException, match="Not Found"):
            client.get_notebook(id="invalid_id")

    def test__update_existing_notebook_metadata__update_notebook_metadata_succeeds(
        self, client: NotebookClient, create_notebook, update_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        [filename, extension] = random_filename.split(".")
        new_name = f"{filename}-updated.{extension}"
        notebook.name = new_name
        notebook.properties = {"key": "value"}

        response = update_notebook(id=notebook.id, metadata=notebook)

        assert response.id == notebook.id
        assert response.name != random_filename
        assert response.name == new_name
        assert response.properties == notebook.properties

    def test__update_existing_notebook_content__update_notebook_content_succeeds(
        self, client: NotebookClient, create_notebook, update_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        with open("tests/integration/notebook/sample_file.ipynb", "rb") as file:
            response = update_notebook(id=notebook.id, content=file)

        assert response.id == notebook.id

    def test__update_notebook_metadata_with_invalid_id__raises_ApiException_NotFound(
        self, client: NotebookClient
    ):
        metadata = NotebookMetadata(name="invalid_name")
        with pytest.raises(ApiException, match="Not Found"):
            client.update_notebook(id="invalid_id", metadata=metadata)

    def test__update_notebook_content_with_invalid_file__raises_ApiException_BadRequest(
        self, client: NotebookClient, create_notebook, update_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        with open("tests/integration/notebook/test_notebook_client.py", "rb") as file:
            with pytest.raises(ApiException, match="Bad Request"):
                update_notebook(id=notebook.id, content=file)

    def test__update_notebook_content_with_duplicate_file_name__raises_ApiException_BadRequest(
        self, client: NotebookClient, create_notebook, update_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        metadata.name = notebook.name = "duplicate_name"
        create_notebook(metadata=metadata)

        with pytest.raises(ApiException, match="409 Conflict"):
            update_notebook(id=notebook.id, metadata=notebook)

    def test__update_notebook_with_invalid_workspace__raises_ApiException_BadRequest(
        self, client: NotebookClient, create_notebook, update_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        metadata.workspace = "invalid_workspace"
        with pytest.raises(ApiException, match="Bad Request"):
            update_notebook(id=notebook.id, metadata=metadata)

    def test__delete_notebook_with_valid_id__notebook_should_delete_successfully(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata, cleanup=False)

        client.delete_notebook(id=notebook.id)

        with pytest.raises(ApiException, match="Not Found"):
            client.get_notebook(id=notebook.id)

    def test__delete_notebook_with_invalid_id__raises_ApiException_NotFound(
        self, client
    ):
        with pytest.raises(ApiException, match="Not Found"):
            client.delete_notebook(id="invalid_id")

    def test__query_notebook_by_id__return_notebook_matches_id(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        request = QueryNotebookRequest(filter=f'id="{notebook.id}"')
        print(request)
        response = client.query_notebooks(request)

        assert response.notebooks is not None
        assert len(response.notebooks) == 1
        assert response.continuation_token is None
        assert response.notebooks[0].id == notebook.id
        assert response.notebooks[0].name == random_filename

    def test__query_notebook_by_invalid_id__returns_empty_list(self, client):
        request = QueryNotebookRequest(filter='id="invalid_id"')
        response = client.query_notebooks(request)

        assert len(response.notebooks) == 0
        assert response.continuation_token is None

    def test__query_notebook_by_name__returns_notebook_matches_name(
        self, client, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        request = QueryNotebookRequest(filter=f'name.StartsWith("{random_filename}")')
        response = client.query_notebooks(request)

        assert len(response.notebooks) == 1
        assert response.continuation_token is None
        assert response.notebooks[0].id == notebook.id
        assert response.notebooks[0].name == random_filename

    def test__query_notebook_by_invalid_name__returns_empty_list(self, client):
        request = QueryNotebookRequest(filter='name="invalid_name"')
        response = client.query_notebooks(request)

        assert len(response.notebooks) == 0
        assert response.continuation_token is None

    def test__query_by_taking_3_notebooks__returns_3_notebooks(self, client):
        request = QueryNotebookRequest(take=3)
        response = client.query_notebooks(request)

        assert len(response.notebooks) == 3
        assert response.continuation_token is not None

    def test__query_notebooks_by_continuation_token__returns_next_page_of_notebooks(
        self, client
    ):
        request = QueryNotebookRequest(take=3)
        response = client.query_notebooks(request)

        assert len(response.notebooks) == 3
        assert response.continuation_token is not None

        request.continuation_token = response.continuation_token
        response = client.query_notebooks(request)

        assert len(response.notebooks) != 0
        assert response.continuation_token is not None

    def test__get_notebook_content_by_id__returns_notebook_content(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        response = client.get_notebook_content(id=notebook.id)

        with open("tests/integration/notebook/sample_file.ipynb", "rb") as file:
            assert response.read() == file.read()

    def test__get_notebook_content_by_invalid_id__raises_ApiException_NotFound(
        self, client
    ):
        with pytest.raises(ApiException, match="Not Found"):
            client.get_notebook_content(id="invalid_id")

    @responses.activate
    def test__create_executions_with_valid_notebook_id__returns_executions_with_right_fields(
        self,
        client: NotebookClient,
    ):
        execution_id_1 = "SomeExecutionId1"
        execution_id_2 = "SomeExecutionId2"

        notebook_id_1 = "SomeNotebookId1"
        notebook_id_2 = "SomeNotebookId2"

        workspace_id = "SomeWorkspaceId"
        return_value = {
            "executions": [
                {
                    "cachedResult": False,
                    "id": execution_id_1,
                    "notebookId": notebook_id_1,
                    "orgId": "f8a1fa16-a180-4a00-b90d-225c0a966848",
                    "userId": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "parameters": {},
                    "workspaceId": workspace_id,
                    "timeout": 3600,
                    "retryCount": 0,
                    "status": "QUEUED",
                    "queuedAt": "2024-12-12T02:34:44.0967706Z",
                    "lastUpdatedBy": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "lastUpdatedTimestamp": "2024-12-12T02:34:44.0967706Z",
                    "errorCode": "NO_ERROR",
                    "reportSettings": {"format": "NO_REPORT", "excludeCode": False},
                    "source": {"type": "MANUAL"},
                    "priority": "MEDIUM",
                    "resourceProfile": "DEFAULT",
                },
                {
                    "cachedResult": False,
                    "id": execution_id_2,
                    "notebookId": notebook_id_2,
                    "orgId": "f8a1fa16-a180-4a00-b90d-225c0a966848",
                    "userId": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "parameters": {},
                    "workspaceId": workspace_id,
                    "timeout": 3600,
                    "retryCount": 0,
                    "status": "QUEUED",
                    "queuedAt": "2024-12-12T02:36:13.7375558Z",
                    "lastUpdatedBy": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "lastUpdatedTimestamp": "2024-12-12T02:36:13.7375558Z",
                    "errorCode": "NO_ERROR",
                    "reportSettings": {"format": "NO_REPORT", "excludeCode": False},
                    "source": {"type": "MANUAL"},
                    "priority": "MEDIUM",
                    "resourceProfile": "DEFAULT",
                },
            ]
        }

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/executions",
            json=return_value,
            status=200,
        )

        request_1 = CreateExecutionRequest(
            notebook_id=notebook_id_1, workspace_id=workspace_id
        )
        request_2 = CreateExecutionRequest(
            notebook_id=notebook_id_2, workspace_id=workspace_id
        )

        response = client.create_executions([request_1, request_2])

        assert response.error is None
        assert response.executions is not None
        assert len(response.executions) == 2
        assert response.executions[0].id == execution_id_1
        assert response.executions[1].id == execution_id_2

        assert all(
            execution.workspace_id is not None
            and execution.notebook_id is not None
            and execution.organization_id is not None
            and execution.user_id is not None
            and execution.status == ExecutionStatus.QUEUED
            and execution.queued_at is not None
            and execution.last_updated_timestamp is not None
            and execution.error_code is not None
            and execution.report_settings is not None
            and execution.source is not None
            and execution.priority is not None
            and execution.resource_profile is not None
            and execution.retry_count == 0
            and execution.last_updated_by is not None
            for execution in response.executions
        )

    @responses.activate
    def test__create_executions_with_valid_notebook_id_invalid_workspace__returns_error_and_valid_executions(
        self,
        client: NotebookClient,
    ):
        execution_id_1 = "SomeExecutionId1"

        notebook_id_1 = "SomeNotebookId1"
        notebook_id_2 = "SomeNotebookId2"

        workspace_id = "SomeWorkspaceId"
        return_value = {
            "executions": [
                {
                    "cachedResult": False,
                    "id": execution_id_1,
                    "notebookId": notebook_id_1,
                    "orgId": "f8a1fa16-a180-4a00-b90d-225c0a966848",
                    "userId": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "parameters": {},
                    "workspaceId": workspace_id,
                    "timeout": 3600,
                    "retryCount": 0,
                    "lastUpdatedBy": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "status": "QUEUED",
                    "queuedAt": "2024-12-12T02:34:44.0967706Z",
                    "lastUpdatedTimestamp": "2024-12-12T02:34:44.0967706Z",
                    "errorCode": "NO_ERROR",
                    "reportSettings": {"format": "NO_REPORT", "excludeCode": False},
                    "source": {"type": "MANUAL"},
                    "priority": "MEDIUM",
                    "resourceProfile": "DEFAULT",
                },
            ],
            "error": {
                "name": "Skyline.OneOrMoreErrorsOccurred",
                "code": -251041,
                "message": "One or more errors occurred. See the contained list for details of each error.",
                "args": [],
                "innerErrors": [
                    {
                        "name": "SkylineWebServices.Unauthorized",
                        "code": -252229,
                        "message": "User is not authorized.",
                        "resourceId": notebook_id_2,
                        "args": [],
                        "innerErrors": [],
                    }
                ],
            },
        }

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/executions",
            json=return_value,
            status=200,
        )

        request_1 = CreateExecutionRequest(
            notebook_id=notebook_id_1, workspace_id=workspace_id
        )
        request_2 = CreateExecutionRequest(
            notebook_id=notebook_id_2, workspace_id="invalid_workspace_id"
        )

        response = client.create_executions([request_1, request_2])

        assert response.error is not None
        assert response.executions is not None
        assert len(response.executions) == 1

    @responses.activate
    def test__create_executions_with_invalid_notebook_id__returns_execution(
        self,
        client: NotebookClient,
    ):
        execution_id = "SomeExecutionId1"
        notebook_id = "InvalidNotebookId"
        workspace_id = "SomeWorkspaceId"

        return_value = {
            "executions": [
                {
                    "cachedResult": False,
                    "id": execution_id,
                    "notebookId": notebook_id,
                    "orgId": "f8a1fa16-a180-4a00-b90d-225c0a966848",
                    "userId": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "parameters": {},
                    "workspaceId": workspace_id,
                    "timeout": 3600,
                    "lastUpdatedBy": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
                    "retryCount": 0,
                    "status": "QUEUED",
                    "queuedAt": "2024-12-12T02:34:44.0967706Z",
                    "lastUpdatedTimestamp": "2024-12-12T02:34:44.0967706Z",
                    "errorCode": "NO_ERROR",
                    "reportSettings": {"format": "NO_REPORT", "excludeCode": False},
                    "source": {"type": "MANUAL"},
                    "priority": "MEDIUM",
                    "resourceProfile": "DEFAULT",
                },
            ]
        }

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/executions",
            json=return_value,
            status=200,
        )

        request_1 = CreateExecutionRequest(
            notebook_id=notebook_id, workspace_id=workspace_id
        )

        response = client.create_executions([request_1])

        assert response.error is None
        assert response.executions is not None
        assert len(response.executions) == 1
        assert response.executions[0].id == execution_id

    @responses.activate
    def test__get_execution_by_id__returns_execution_with_right_fields(
        self,
        client: NotebookClient,
    ):
        execution_id = "SomeExecutionId1"
        return_value = {
            "id": execution_id,
            "notebookId": "fa479189-d26a-4521-a751-173355a811ce",
            "orgId": "f8a1fa16-a180-4a00-b90d-225c0a966848",
            "userId": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
            "parameters": {},
            "workspaceId": "846e294a-a007-47ac-9fc2-fac07eab240e",
            "timeout": 3600,
            "status": "FAILED",
            "lastUpdatedBy": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
            "retryCount": 0,
            "queuedAt": "2024-12-12T02:46:20.193Z",
            "startedAt": "2024-12-12T02:46:20.202Z",
            "completedAt": "2024-12-12T02:46:50.506Z",
            "lastUpdatedTimestamp": "2024-12-12T02:46:50.506Z",
            "exception": "An error occurred while executing the notebook.",
            "errorCode": "NOTEBOOK_ERROR",
            "reportSettings": {"format": "NO_REPORT", "excludeCode": False},
            "source": {"type": "MANUAL"},
            "priority": "MEDIUM",
            "resourceProfile": "DEFAULT",
        }

        responses.add(
            responses.GET,
            f"{BASE_URL}/ninbexecution/v1/executions/SomeExecutionId1",
            json=return_value,
            status=200,
        )

        execution = client.get_execution_by_id(id=execution_id)

        assert execution.id == execution_id
        assert execution.workspace_id is not None
        assert execution.notebook_id is not None
        assert execution.organization_id is not None
        assert execution.user_id is not None
        assert execution.status is not None
        assert execution.queued_at is not None
        assert execution.last_updated_timestamp is not None
        assert execution.error_code is not None
        assert execution.report_settings is not None
        assert execution.source is not None
        assert execution.priority is not None
        assert execution.resource_profile is not None
        assert execution.last_updated_by is not None
        assert execution.retry_count is not None

    def test__get_execution_by_invalid_id__raises_ApiException_NotFound(
        self,
        client: NotebookClient,
    ):
        with pytest.raises(ApiException, match="Not Found"):
            client.get_execution_by_id(id="InvalidExecutionId")

    @responses.activate
    def test__filter_executions_by_status__returns_executions_matches_status(
        self,
        client: NotebookClient,
    ):
        return_value = {
            "id": "execution_id",
            "notebookId": "fa479189-d26a-4521-a751-173355a811ce",
            "orgId": "f8a1fa16-a180-4a00-b90d-225c0a966848",
            "userId": "7aac74e0-10f7-4a07-93df-d7304a1ed177",
            "parameters": {},
            "workspaceId": "846e294a-a007-47ac-9fc2-fac07eab240e",
            "timeout": 3600,
            "status": "FAILED",
            "queuedAt": "2024-12-12T02:46:20.193Z",
            "startedAt": "2024-12-12T02:46:20.202Z",
            "completedAt": "2024-12-12T02:46:50.506Z",
            "lastUpdatedTimestamp": "2024-12-12T02:46:50.506Z",
            "exception": "An error occurred while executing the notebook.",
            "errorCode": "NOTEBOOK_ERROR",
            "reportSettings": {"format": "NO_REPORT", "excludeCode": False},
            "source": {"type": "MANUAL"},
            "priority": "MEDIUM",
            "resourceProfile": "DEFAULT",
        }

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/query-executions",
            json=return_value,
            status=200,
        )
        query = QueryExecutionsRequest(
            filter=f"status = {ExecutionStatus.FAILED.value}"
        )
        response = client.query_executions(query)

        assert len(response) == 1

        assert response[0].status == ExecutionStatus.FAILED

    def test__query_executions_by_invalid_filter__raises_ApiException_BadRequest(
        self,
        client: NotebookClient,
    ):

        query = QueryExecutionsRequest(filter="status = 'INVALID_STATUS'")

        with pytest.raises(ApiException, match="Bad Request"):
            client.query_executions(query)

    @responses.activate
    def test__query_executions_by_projection__returns_executions_with_projected_properties(
        self, client: NotebookClient
    ):
        return_value = [
            {
                "id": "execution_id_1",
                "status": "IN_PROGRESS",
            },
            {
                "id": "execution_id_2",
                "status": "TIMED_OUT",
            },
            {
                "id": "execution_id_3",
                "status": "FAILED",
            },
        ]

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/query-executions",
            json=return_value,
            status=200,
        )

        query = QueryExecutionsRequest(
            projection=[ExecutionField.ID, ExecutionField.STATUS]
        )
        response = client.query_executions(query)

        assert all(
            execution.id is not None
            and execution.status is not None
            and execution.workspace_id is None
            and execution.notebook_id is None
            and execution.organization_id is None
            and execution.user_id is None
            and execution.queued_at is None
            and execution.last_updated_timestamp is None
            and execution.error_code is None
            and execution.report_settings is None
            and execution.source is None
            and execution.priority is None
            and execution.resource_profile is None
            for execution in response
        )

    @responses.activate
    def test__query_executions_by_status_in_ascending__returns_executions_sorted_by_status(
        self, client: NotebookClient
    ):
        return_value = [
            {
                "id": "execution_id_1",
                "status": "IN_PROGRESS",
            },
            {
                "id": "execution_id_2",
                "status": "TIMED_OUT",
            },
            {
                "id": "execution_id_3",
                "status": "FAILED",
            },
        ]

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/query-executions",
            json=return_value,
            status=200,
        )

        query = QueryExecutionsRequest(
            order_by=ExecutionSortField.STATUS,
            projection=[ExecutionField.ID, ExecutionField.STATUS],
        )
        response = client.query_executions(query)

        assert response[0].status == ExecutionStatus.IN_PROGRESS
        assert response[1].status == ExecutionStatus.TIMED_OUT
        assert response[2].status == ExecutionStatus.FAILED

    @responses.activate
    def test__query_executions_by_status_in_descending__returns_executions_sorted_by_status(
        self, client: NotebookClient
    ):
        return_value = [
            {
                "id": "execution_id_1",
                "status": "FAILED",
            },
            {
                "id": "execution_id_2",
                "status": "TIMED_OUT",
            },
            {
                "id": "execution_id_3",
                "status": "IN_PROGRESS",
            },
        ]

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/query-executions",
            json=return_value,
            status=200,
        )

        query = QueryExecutionsRequest(
            order_by=ExecutionSortField.STATUS,
            projection=[ExecutionField.ID, ExecutionField.STATUS],
            descending=True,
        )
        response = client.query_executions(query)

        assert response[0].status == ExecutionStatus.FAILED
        assert response[1].status == ExecutionStatus.TIMED_OUT
        assert response[2].status == ExecutionStatus.IN_PROGRESS

    @responses.activate
    def test__cancel_executions__return_inner_errors(self, client: NotebookClient):
        return_value = {
            "innerErrors": ["Error1", "Error2"],
        }

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/cancel-executions",
            json=return_value,
            status=200,
        )

        response = client.cancel_executions(["execution_id_1", "execution_id_2"])

        print(response)
        assert response["innerErrors"] == ["Error1", "Error2"]

    @responses.activate
    def test__retry_executions__return_inner_errors(self, client: NotebookClient):
        return_value = {
            "innerErrors": ["Error1", "Error2"],
        }

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/retry-executions",
            json=return_value,
            status=200,
        )

        response = client.retry_executions(["execution_id_1", "execution_id_2"])

        print(response)
        assert response["innerErrors"] == ["Error1", "Error2"]

    @responses.activate
    def test__create_executions_from_existing__return_inner_errors(
        self, client: NotebookClient
    ):
        return_value = {
            "innerErrors": ["Error1", "Error2"],
        }

        responses.add(
            responses.POST,
            f"{BASE_URL}/ninbexecution/v1/retry-executions",
            json=return_value,
            status=200,
        )

        response = client.retry_executions(["execution_id_1", "execution_id_2"])

        print(response)
        assert response["innerErrors"] == ["Error1", "Error2"]
