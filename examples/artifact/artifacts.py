import io

from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.core import HttpConfiguration

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

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
client.delete_artifact(artifact_id)
