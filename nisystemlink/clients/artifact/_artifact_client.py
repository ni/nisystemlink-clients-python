"""Implementation of ArtifactClient"""

from typing import Optional

from httpcore import Response

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
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
    
    @get("")
    def api_info(self) -> models.V1Operations:
        """Get information about available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the Notebook execution Service.
        """
        ...

    @post("artifacts")
    def upload_artifact(
        self,
        workspace: Part,
        artifact: Part
    ) -> models.UploadArtifactResponse:
        """Uploads an artifact.

        Args:
            request: The request containing the workspace id and artifact content to upload.

        Returns:
            The response containing the artifact ID.

        Raises:
            ArtifactError: if unable to upload the artifact.
        """
        ...

    @get("artifacts/{artifact_id}")
    def download_artifact(
        self, artifact_id: Path
    ) -> Response:
        """Downloads an artifact.

        Args:
            artifact_id: The ID of the artifact to download.

        Returns:
            The response containing the file content.

        Raises:
            ArtifactError: if unable to download the artifact.
        """
        ...