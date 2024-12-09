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
        metadata: NotebookMetadata,
    ) -> NotebookMetadata:

        # file_bytes = file.read()  # Read file as bytes
        with open("tests/integration/notebook/test_file.ipynb", "rb") as file:
            notebook_response = client.create_notebook(metadata=metadata, content=file)
        notebook_ids.append(notebook_response.id)

        return notebook_response

    yield _create_notebook

    if notebook_ids:
        for notebook_id in filter(None, notebook_ids):
            client.delete_notebook(id=notebook_id)


@pytest.mark.enterprise
@pytest.mark.integration
class TestNotebookClient:
    def test__create_notebook__succeeds(self, create_notebook, random_filename):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        assert notebook.name == random_filename

    def test__get_notebook_with_valid_id__returns_notebook_with_right_field_values(
        self, client, create_notebook, random_filename
    ):
        # metadata = NotebookMetadata(name=random_filename)
        # notebook = create_notebook(metadata=metadata)

        response = client.get_notebook(id="db839861-cac4-4b0e-a827-975be72c6404")

        assert response.id == "db839861-cac4-4b0e-a827-975be72c6404"
        assert response.workspace is not None
        assert response.created_by is not None
        assert response.created_at is not None
        # assert response.name == notebook.name == random_filename

    def test__get_notebook_with_invalid_id__raises_ApiException_NotFound(self, client):
        with pytest.raises(ApiException, match="Not Found"):
            client.get_notebook(id="invalid_id")

    def test__update_notebook__succeeds(self, client, create_notebook, random_filename):
        # metadata = NotebookMetadata(name=random_filename)
        # notebook = create_notebook(metadata=metadata)

        [filename, extension] = random_filename.split(".")
        new_name = f"{filename}-updated.{extension}"
        notebook = {"name": new_name}

        response = client.update_notebook(
            id="db839861-cac4-4b0e-a827-975be72c6404", metadata=notebook
        )

        assert response.id == "db839861-cac4-4b0e-a827-975be72c6404"
        assert response.name != random_filename
        assert response.name == new_name

    def test__delete_notebook_with_valid_id__notebook_should_delete_successfully(
        self, client, create_notebook, random_filename
    ):
        # metadata = NotebookMetadata(name=random_filename)
        # notebook = create_notebook(metadata=metadata)

        client.delete_notebook(id="d948c520-a579-4b53-b710-c5495c4bc951")

        with pytest.raises(ApiException, match="Not Found"):
            client.get_notebook(id="d948c520-a579-4b53-b710-c5495c4bc951")

    def test__delete_notebook_with_invalid_id__raises_ApiException_NotFound(
        self, client
    ):
        with pytest.raises(ApiException, match="Not Found"):
            client.delete_notebook(id="invalid_id")

    def test__query_notebook_by_id__return_notebook_matches_id(
        self, client, create_notebook, random_filename
    ):
        # metadata = NotebookMetadata(name=random_filename)
        # notebook = create_notebook(metadata=metadata)

        request = QueryNotebookRequest(
            filter=f'id="2f3b45c0-7be0-4e3d-8adc-7a031da8fc6c"'
        )
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 1
        assert response.continuation_token is None
        # assert response.notebook[0].id == notebook.id
        # assert response.notebook[0].name == random_filename
        # assert response.notebook[0].properties is not None

    def test__query_notebook_by_invalid_id__returns_empty_list(self, client):
        request = QueryNotebookRequest(filter=f'id="invalid_id"')
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 0
        assert response.continuation_token is None

    def test__query_notebook_by_name__returns_notebook_matches_name(
        self, client, create_notebook, random_filename
    ):
        # metadata = NotebookMetadata(name=random_filename)
        # notebook = create_notebook(metadata=metadata)

        request = QueryNotebookRequest(filter=f'name.StartsWith("My_1121notebook")')
        response = client.query_notebooks_paged(request)

        assert len(response.notebooks) == 1
        assert response.continuation_token is None
        # assert response.notebook[0].id == notebook.id
        # assert response.notebook[0].name == random_filename
        # assert response.notebook[0].properties is not None

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

    def test__get_notebook_content_by_id__returns_notebook_content(self, client):
        response = client.get_notebook_content(
            id="2f3b45c0-7be0-4e3d-8adc-7a031da8fc6c"
        )

        assert response.read() == TEST_FILE_DATA

    def test__get_notebook_content_by_invalid_id__raises_ApiException_NotFound(
        self, client
    ):
        with pytest.raises(ApiException, match="Not Found"):
            client.get_notebook_content(id="invalid_id")
