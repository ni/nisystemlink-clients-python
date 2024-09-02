import pytest
import os
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.artifact.models import UploadArtifactResponse


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> ArtifactClient:
    """Fixture to create an ArtifactClient instance."""
    return ArtifactClient(enterprise_config)

@pytest.mark.integration
@pytest.mark.enterprise
class TestArtifact:

    def test__upload_artifact__artifact_uploaded(self, client: ArtifactClient):
        workspace = os.getenv("SYSTEMLINK_WORKSPACE_ID")
        artifact_content = b"test content"
        response = client.upload_artifact(workspace=workspace, artifact=artifact_content)
        assert response is not None
        assert response.id is not None

    def test__download_artifact__artifact_downloaded(self, client: ArtifactClient):
        workspace = os.getenv("SYSTEMLINK_WORKSPACE_ID")
        artifact_content = b"test content"
        upload_response = client.upload_artifact(workspace=workspace, artifact=artifact_content)
        artifact_id = upload_response.id

        download_response = client.download_artifact(artifact_id)
        assert download_response is not None
        assert download_response.content == artifact_content