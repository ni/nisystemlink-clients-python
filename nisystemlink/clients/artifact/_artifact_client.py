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

    @post("artifacts")
    def upload_artifact(
        self,
        workspace: Part,
        artifact: Part
    ) -> models.UploadArtifactResponse:
        """Uploads an artifact.

        Args:
            workspace: The workspace containing the artifact.
            artifact: The artifact to upload.

        Returns:
            UploadArtifactResponse: The response containing the artifact ID.

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

        """
        ...