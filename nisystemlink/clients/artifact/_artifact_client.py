"""Implementation of ArtifactClient"""

from typing import BinaryIO, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post, response_handler
from nisystemlink.clients.core.helpers._iterator_file_like import IteratorFileLike
from requests.models import Response
from uplink import Part, Path

from . import models


class ArtifactClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
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

    @post("artifacts")
    def __upload_artifact(
        self, workspace: Part, artifact: Part
    ) -> models.UploadArtifactResponse:
        """Uploads an artifact  using multipart/form-data headers to send the file payload in the HTTP body.

        Args:
            workspace: The workspace containing the artifact.
            artifact: The artifact to upload.

        Returns:
            UploadArtifactResponse: The response containing the artifact ID.

        """

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

    def _iter_content_filelike_wrapper(response: Response) -> IteratorFileLike:
        return IteratorFileLike(response.iter_content(chunk_size=4096))

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
