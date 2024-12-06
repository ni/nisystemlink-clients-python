from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.notebook import NotebookClient
from nisystemlink.clients.notebook.models import NotebookMetadata, QueryNotebookRequest

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = NotebookClient(configuration=server_configuration)

# Create a notebook with metadata and content
metadata = NotebookMetadata(
    name="Example Notebook",
    parameters={"param1": "value1"},
    properties={"property1": "value1"},
)

with open("example.ipynb", "rb") as file:
    encoded_file = file.read().decode("utf-8")
notebook_response = client.create_notebook(metadata=metadata, content=encoded_file)

# Get the notebook by ID
notebook = client.get_notebook(notebook_response.id or "your_notebook_id")

# Update the notebook with new metadata and content
metadata = NotebookMetadata(
    name="Updated Example Notebook",
    parameters={"param1": "value2"},
    properties={"property1": "value2"},
)

with open("example_updated.ipynb", "rb") as file:
    encoded_file = file.read().decode("utf-8")
notebook_response = client.update_notebook(
    id=notebook_response.id or "your_notebook_id",
    metadata=metadata,
    content=encoded_file,
)

# Get notebook content by ID
notebook_content = client.get_notebook_content(
    notebook_response.id or "your_notebook_id"
)

# Query notebook by name
query_request = QueryNotebookRequest(
    filter="name='Example Notebook'",
)

query_response = client.query_notebooks_paged(query_request)

# Query notebooks by take
query_request = QueryNotebookRequest(take=2)
query_response = client.query_notebooks_paged(query_request)

query_request = QueryNotebookRequest(
    continuation_token=query_response.continuation_token,
    take=1,
)
query_response = client.query_notebooks_paged(query_request)

# Delete the notebook by ID
client.delete_notebook(notebook_response.id or "your_notebook_id")
