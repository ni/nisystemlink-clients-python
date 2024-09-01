import pytest
import os
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.artifact.models import UploadArtifactResponse
from httpcore import Response

@pytest.fixture(scope="class")
def artifact_client(enterprise_config: HttpConfiguration) -> ArtifactClient:
    """Fixture to create an ArtifactClient instance."""
    return ArtifactClient(enterprise_config)

@pytest.fixture
def upload_artifact(artifact_client: ArtifactClient):
    """Fixture to upload an artifact and clean up after tests."""
    uploaded_artifacts = []

    def _upload_artifact(workspace: str, artifact_content: bytes) -> UploadArtifactResponse:
        response = artifact_client.upload_artifact(workspace=workspace, artifact=artifact_content)
        uploaded_artifacts.append(response.artifact_id)
        return response

    yield _upload_artifact

@pytest.mark.integration
@pytest.mark.enterprise
class TestArtifact:
    def test_api_info(self, artifact_client: ArtifactClient):
        response = artifact_client.api_info()
        assert response is not None
    # def test__api_info__returns(self, client: ArtifactClient):
    #     response = client.api_info()
    #     assert len(response.dict()) != 0

    def test_upload_artifact(self, artifact_client: ArtifactClient, upload_artifact):
        workspace = "test_workspace"
        artifact_content = b"test content"
        response = upload_artifact(workspace, artifact_content)
        assert response is not None
        assert response.artifact_id is not None

    def test_download_artifact(self, artifact_client: ArtifactClient, upload_artifact):
        workspace = "test_workspace"
        artifact_content = b"test content"
        upload_response = upload_artifact(workspace, artifact_content)
        artifact_id = upload_response.artifact_id

        download_response = artifact_client.download_artifact(artifact_id)
        assert download_response is not None
        assert download_response.content == artifact_content