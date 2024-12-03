import io
import string
from random import choices

import pytest
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.notebook import NotebookClient
from nisystemlink.clients.notebook.models import NotebookMetadata

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


def create_notebook(client: NotebookClient):
    """Fixture to return a factory that creates a notebook."""
    notebook_ids = []

    def _create_notebook(
        metadata: NotebookMetadata, test_file_data: bytes = TEST_FILE_DATA
    ) -> NotebookMetadata:
        test_file = io.BytesIO(test_file_data)
        notebook_response = client.create_notebook(metadata=metadata, content=test_file)
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

    def test__get_notebook__succeeds(self, client, create_notebook, random_filename):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        response = client.get_notebook(id=notebook.id)

        assert response.id == notebook.id
        assert response.name == notebook.name == random_filename

    def test__update_notebook__succeeds(self, client, create_notebook, random_filename):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        [filename, extension] = random_filename.split(".")
        new_name = f"{filename}-updated.{extension}"
        notebook.name = new_name

        response = client.update_notebook(id=notebook.id, metadata=notebook)

        assert response.id == notebook.id
        assert response.name != random_filename
        assert response.name == new_name

    def test__delete_notebook__succeeds(self, client, create_notebook, random_filename):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        client.delete_notebook(id=notebook.id)

        with pytest.raises(ApiException):
            client.get_notebook(id=notebook.id)

    def test__query_notebooks__succeeds(self, client, create_notebook, random_filename):
        metadata = NotebookMetadata(name=random_filename)
        notebook = create_notebook(metadata=metadata)

        response = client.query_notebooks(filter=f"name = '{random_filename}'")

        assert response.total_count == 1
        assert len(response.notebook) == 1
        assert response.notebook[0].id == notebook.id
        assert response.notebook[0].name == random_filename
        assert response.notebook[0].properties is not None
        assert response.notebook[0].properties["Name"] == random_filename
