import io

from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.core._api_exception import ApiException


# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = ArtifactClient(configuration=server_configuration)

# Define the workspace and artifact content
workspace = "your workspace ID"
artifact_stream = io.BytesIO(b"test content")

# Upload the artifact
upload_response = client.upload_artifact(workspace=workspace, artifact=artifact_stream)
if upload_response and upload_response.id:
    print(f"Uploaded artifact ID: {upload_response.id}")

# Download the artifact using the ID from the upload response
artifact_id = upload_response.id
download_response = client.download_artifact(artifact_id)
if download_response:
    downloaded_content = download_response.read()
    print(f"Downloaded artifact content: {downloaded_content.decode('utf-8')}")

# Delete the artifact
try:
    client.delete_artifact(artifact_id)
    print(f"Successfully deleted artifact with ID: {artifact_id}")
except ApiException as api_exception:
    print(f"Failed to delete artifact with ID {artifact_id}: {api_exception}")
