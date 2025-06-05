import io
import os
from typing import List

import pytest
from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.artifact.models._upload_artifact_response import (
    UploadArtifactResponse,
)
from nisystemlink.clients.core._api_exception import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> ArtifactClient:
    """Fixture to create an ArtifactClient instance."""
    return ArtifactClient(enterprise_config)


def get_workspace() -> str:
    """Get the workspace ID from environment variables or skip the test if not set."""
    workspace = os.getenv("SYSTEMLINK_WORKSPACE_ID")
    if workspace is None:
        pytest.skip("SYSTEMLINK_WORKSPACE_ID environment variable is not set.")

    return workspace


@pytest.fixture
def create_artifact(client: ArtifactClient):
    """Fixture to return a factory that creates artifact."""
    created_artifact_ids: List[str] = []

    def _create_artifact(content: bytes = b"test content"):
        workspace = get_workspace()
        artifact_stream = io.BytesIO(content)
        response = client.upload_artifact(workspace=workspace, artifact=artifact_stream)
        created_artifact_ids.append(response.id)

        return response

    yield _create_artifact

    for artifact_id in created_artifact_ids:
        try:
            client.delete_artifact(artifact_id)
        except ApiException as api_exception:
            if api_exception.http_status_code != 404:
                raise api_exception


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
        upload_response: UploadArtifactResponse = create_artifact()
        artifact_id = upload_response.id

        delete_response = client.delete_artifact(artifact_id)

        assert delete_response is None
