"""Implementation of ArtifactClient"""

from typing import BinaryIO

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import (
    delete,
    get,
    post,
    response_handler,
)
from nisystemlink.clients.core._uplink._multipart_retry import (
    retryable_multipart_request,
)
from nisystemlink.clients.core.helpers._iterator_file_like import IteratorFileLike
from requests.models import Response
from uplink import Part, Path, retry

from . import models


def _iter_content_filelike_wrapper(response: Response) -> IteratorFileLike:
    return IteratorFileLike(response.iter_content(chunk_size=4096))


@retry(when=retry.when.status(429), stop=retry.stop.after_attempt(5))
class ArtifactClient(BaseClient):
    def __init__(self, configuration: core.HttpConfiguration | None = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the  Notebook execution Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/ninbartifact/v1/")

    @retryable_multipart_request()
    @post("artifacts", args=[Part("workspace"), Part("artifact")])
    def __upload_artifact(
        self, workspace: str, artifact: BinaryIO
    ) -> models.UploadArtifactResponse:
        """Uploads an artifact  using multipart/form-data headers to send the file payload in the HTTP body.

        Args:
            workspace: The workspace containing the artifact.
            artifact: The artifact to upload.

        Returns:
            UploadArtifactResponse: The response containing the artifact ID.

        """
        ...

    def upload_artifact(
        self, workspace: str, artifact: BinaryIO
    ) -> models.UploadArtifactResponse:
        """Uploads an artifact.

        Args:
            workspace: The workspace containing the artifact.
            artifact: The artifact to upload.

        Returns:
            UploadArtifactResponse: The response containing the artifact ID.

        """
        response = self.__upload_artifact(
            workspace=workspace,
            artifact=artifact,
        )

        return response

    @response_handler(_iter_content_filelike_wrapper)
    @get("artifacts/{id}")
    def download_artifact(self, id: Path) -> IteratorFileLike:
        """Downloads an artifact.

        Args:
            id: The ID of the artifact to download.

        Returns:
            A file-like object for reading the artifact content.

        """
        ...

    @delete("artifacts/{id}", args=[Path("id")])
    def delete_artifact(self, id: str) -> None:
        """Deletes an artifact.

        Args:
            id: The ID of the artifact to delete.

        """
        ...
