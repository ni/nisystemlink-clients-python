import io
import os

import pytest
from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> ArtifactClient:
    """Fixture to create an ArtifactClient instance."""
    return ArtifactClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestArtifact:

    def test__upload_artifact__artifact_uploaded(self, client: ArtifactClient):
        workspace = os.getenv("SYSTEMLINK_WORKSPACE_ID")

        if workspace is not None:
            artifact_stream = io.BytesIO(b"test content")

            response = client.upload_artifact(
                workspace=workspace, artifact=artifact_stream
            )

            assert response is not None
            assert response.id is not None

    def test__download_artifact__artifact_downloaded(self, client: ArtifactClient):
        workspace = os.getenv("SYSTEMLINK_WORKSPACE_ID")

        if workspace is not None:
            artifact_content = b"test content"
            artifact_stream = io.BytesIO(artifact_content)

            upload_response = client.upload_artifact(
                workspace=workspace, artifact=artifact_stream
            )
            artifact_id = upload_response.id
            download_response = client.download_artifact(artifact_id)

            assert download_response is not None
            assert download_response.read() == artifact_content
