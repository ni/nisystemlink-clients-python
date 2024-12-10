import io
import os
import base64
import string
from random import choices

import pytest
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.notebook import NotebookClient
from nisystemlink.clients.notebook.models import NotebookMetadata, QueryNotebookRequest

TEST_FILE_DATA = b"This is a test notebook binary content."
PREFIX = "Notebook Client Tests-"


@pytest.fixture(scope="class")
def client(enterprise_config) -> NotebookClient:
    """Fixture to create a NotebookClient instance."""
    return NotebookClient(enterprise_config)


@pytest.fixture()
def random_filename() -> str:
    """Generate a random filename for each test in test class."""
    rand_file_name = "".join(choices(string.ascii_letters + string.digits, k=10))

    return f"{PREFIX}{rand_file_name}.ipynb"


@pytest.fixture()
def create_notebook(client: NotebookClient):
    """Fixture to return a factory that creates a notebook."""
    notebook_ids = []

    def _create_notebook(
        metadata: NotebookMetadata, cleanup: bool = True
    ) -> NotebookMetadata:

        # file_bytes = file.read()  # Read file as bytes
        with open("tests/integration/notebook/sample_file.ipynb", "rb") as file:
            notebook_response = client.create_notebook(metadata=metadata, content=file)
        if cleanup:
            notebook_ids.append(notebook_response.id)

        return notebook_response

    yield _create_notebook

    if notebook_ids:
        for notebook_id in filter(None, notebook_ids):
            client.delete_notebook(id=notebook_id)


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
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        [filename, extension] = random_filename.split(".")
        new_name = f"{filename}-updated.{extension}"
        notebook.name = new_name
        notebook.properties = {"key": "value"}

        response = client.update_notebook(id=notebook.id, metadata=notebook)

        assert response.id == notebook.id
        assert response.name != random_filename
        assert response.name == new_name
        assert response.properties == notebook.properties

    def test__update_existing_notebook_content__update_notebook_content_succeeds(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        with open("tests/integration/notebook/sample_file.ipynb", "rb") as file:
            response = client.update_notebook(id=notebook.id, content=file)

        assert response.id == notebook.id

    def test__update_notebook_metadata_with_invalid_id__raises_ApiException_NotFound(
        self, client: NotebookClient
    ):
        metadata = NotebookMetadata(name="invalid_name")
        with pytest.raises(ApiException, match="Not Found"):
            client.update_notebook(id="invalid_id", metadata=metadata)

    def test__update_notebook_content_with_invalid_file__raises_ApiException_BadRequest(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        with open("tests/integration/notebook/test_notebook_client.py", "rb") as file:
            with pytest.raises(ApiException, match="Bad Request"):
                client.update_notebook(id=notebook.id, content=file)

    def test__update_notebook_content_with_duplicate_file_name__raises_ApiException_BadRequest(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        metadata.name = notebook.name = "duplicate_name"
        create_notebook(metadata=metadata)

        with pytest.raises(ApiException, match="409 Conflict"):
            client.update_notebook(id=notebook.id, metadata=notebook)

    def test__update_notebook_with_invalid_workspace__raises_ApiException_BadRequest(
        self, client: NotebookClient, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        metadata.workspace = "invalid_workspace"
        with pytest.raises(ApiException, match="Bad Request"):
            client.update_notebook(id=notebook.id, metadata=metadata)

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
        response = client.query_notebooks_paged(request)

        assert response.notebooks is not None
        assert len(response.notebooks) == 1
        assert response.continuation_token is None
        assert response.notebooks[0].id == notebook.id
        assert response.notebooks[0].name == random_filename

    def test__query_notebook_by_invalid_id__returns_empty_list(self, client):
        request = QueryNotebookRequest(filter=f'id="invalid_id"')
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 0
        assert response.continuation_token is None

    def test__query_notebook_by_name__returns_notebook_matches_name(
        self, client, create_notebook, random_filename
    ):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        request = QueryNotebookRequest(filter=f'name.StartsWith("{random_filename}")')
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 1
        assert response.continuation_token is None
        assert response.notebooks[0].id == notebook.id
        assert response.notebooks[0].name == random_filename

    def test__query_notebook_by_invalid_name__returns_empty_list(self, client):
        request = QueryNotebookRequest(filter=f'name="invalid_name"')
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 0
        assert response.continuation_token is None

    def test__query_by_taking_3_notebooks__returns_3_notebooks(self, client):
        request = QueryNotebookRequest(take=3)
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 3
        assert response.continuation_token is not None

    def test__query_notebooks_by_continuation_token__returns_next_page_of_notebooks(
        self, client
    ):
        request = QueryNotebookRequest(take=3)
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 3
        assert response.continuation_token is not None

        request.continuation_token = response.continuation_token
        response = client.query_notebooks_paged(request)

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
