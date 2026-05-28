import io
from typing import List

import pytest
import responses
from nisystemlink.clients.artifact import ArtifactClient
from nisystemlink.clients.artifact.models._upload_artifact_response import (
    UploadArtifactResponse,
)
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from responses import PassthroughResponse
from responses.registries import OrderedRegistry
from uplink.clients.io import blocking_strategy as uplink_blocking_strategy

BASE_URL = "https://test-api.lifecyclesolutions.ni.com"
DEFAULT_WORKSPACE = "2300760d-38c4-48a1-9acb-800260812337"


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> ArtifactClient:
    """Fixture to create an ArtifactClient instance."""
    return ArtifactClient(enterprise_config)


@pytest.fixture
def create_artifact(client: ArtifactClient):
    """Fixture to return a factory that creates artifact."""
    created_artifact_ids: List[str] = []

    def _create_artifact(
        content: bytes = b"test content",
        cleanup: bool = True,
        workspace: str = DEFAULT_WORKSPACE,
    ):
        # Used the main-test default workspace since the client for creating a workspace has not been added yet
        artifact_stream = io.BytesIO(content)
        response = client.upload_artifact(workspace=workspace, artifact=artifact_stream)
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

    def test__upload_artifact_after_rate_limit_retry__artifact_uploaded(
        self, create_artifact, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(uplink_blocking_strategy.time, "sleep", lambda _: None)

        with responses.RequestsMock(registry=OrderedRegistry) as request_mock:
            request_mock.add(
                responses.POST,
                f"{BASE_URL}/ninbartifact/v1/artifacts",
                status=429,
            )
            request_mock.add(
                PassthroughResponse(
                    responses.POST,
                    f"{BASE_URL}/ninbartifact/v1/artifacts",
                )
            )

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
