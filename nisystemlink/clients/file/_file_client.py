"""Implementation of FileClient."""

from typing import Dict, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import (
    delete,
    get,
    post,
    response_handler,
)
from nisystemlink.clients.core.helpers import IteratorFileLike
from requests.models import Response
from uplink import Body, multipart, params, Part, Path, Query

from . import models


def _iter_content_filelike_wrapper(response: Response) -> IteratorFileLike:
    return IteratorFileLike(response.iter_content(chunk_size=4096))


class FileClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`JupyterHttpConfiguration <nisystemlink.clients.core.JupyterHttpConfiguration>`
                is used.

        Raises:
            ApiException: if unable to communicate with the FileClient Service.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, "/nifile/v1/")

    @get("")
    def api_info(self) -> models.V1Operations:
        """Get information about available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the FileClient Service.
        """
        ...

    @get("service-groups")
    def get_service_groups(self):
        """Get list of service groups.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the FileClient Service.
        """
        ...

    @get(
        "service-groups/Default/files",
        args=[
            Query,
            Query,
            Query,
            Query(name="orderBy"),
            Query(name="orderByDescending"),
        ],
    )
    def get_files(
        self,
        id: str,
        skip: int = 0,
        take: int = 0,
        order_by: models.OrderBy = models.OrderBy.CREATED,
        order_by_descending: bool = False,
    ):
        """Lists available files on the SystemLink File service.
        Use the skip and take parameters to return paged responses.
        The orderBy and orderByDescending fields can be used to manage sorting the list by metadata objects.
        """
        ...

    @delete("service-groups/Default/files/{id}", args=[Path, Query])
    def delete_file(self, id: str, force: bool = False):
        """Deletes the file indicated by the resource ID."""
        ...

    @post("service-groups/Default/delete-files", args=[Body, Query])
    def delete_files(self, files: models.DeleteMutipleRequest, force: bool = False):
        ...

    @params({"inline": True})
    @response_handler(_iter_content_filelike_wrapper)
    @get("service-groups/Default/files/{id}/data")
    def download_file(self, id: str) -> IteratorFileLike:
        """Downloads a file from the SystemLink File service."""
        ...

    @multipart
    @post(
        "service-groups/Default/upload-files",
        args=[Part, Part, Query(name="workspace"), Part],
    )
    def upload_file(
        self, file: Part, metadata: Dict[str, str], workspace_id: str, id: str = None
    ) -> models.UploadedFileInfo:
        """Uploads a file using to the SystemLink File service."""
        ...
