import io
from typing import List

import pytest
from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.artifact.models._upload_artifact_response import (
    UploadArtifactResponse,
)
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> ArtifactClient:
    """Fixture to create an ArtifactClient instance."""
    return ArtifactClient(enterprise_config)


@pytest.fixture
def create_artifact(client: ArtifactClient):
    """Fixture to return a factory that creates artifact."""
    created_artifact_ids: List[str] = []

    def _create_artifact(content: bytes = b"test content", cleanup: bool = True):
        artifact_stream = io.BytesIO(content)
        response = client.upload_artifact(
            workspace="2300760d-38c4-48a1-9acb-800260812337", artifact=artifact_stream
        )
        if cleanup:
            created_artifact_ids.append(response.id)

        return response

    yield _create_artifact

    for artifact_id in created_artifact_ids:
        client.delete_artifact(artifact_id)


@pytest.mark.integration
@pytest.mark.enterprise
class TestArtifact:

    def test__upload_artifact__artifact_uploaded(
        self, client: ArtifactClient, create_artifact
    ):
        upload_response: UploadArtifactResponse = create_artifact()

        assert upload_response is not None
        assert upload_response.id is not None

    def test__download_artifact__artifact_downloaded(
        self, client: ArtifactClient, create_artifact
    ):
        artifact_content = b"test content"

        upload_response: UploadArtifactResponse = create_artifact(
            content=artifact_content
        )
        artifact_id = upload_response.id
        download_response = client.download_artifact(artifact_id)

        assert download_response is not None
        assert download_response.read() == artifact_content

    def test__delete_artifact__artifact_deleted(
        self, client: ArtifactClient, create_artifact
    ):
        upload_response: UploadArtifactResponse = create_artifact(cleanup=False)
        artifact_id = upload_response.id

        delete_response = client.delete_artifact(artifact_id)

        assert delete_response is None
