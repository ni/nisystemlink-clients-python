"""Implementation of FileClient."""

import json
from typing import BinaryIO, Dict, List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._file_like_response import (
    file_like_response_handler,
)
from nisystemlink.clients.core._uplink._methods import (
    delete,
    get,
    post,
    response_handler,
)
from nisystemlink.clients.core.helpers import IteratorFileLike
from requests.models import Response
from uplink import Body, Field, params, Part, Path, Query, retry

from . import models


def _file_uri_response_handler(response: Response) -> str:
    """Response handler for File URI response. Extracts ID from URI."""
    resp = response.json()
    uri: str = resp["uri"]
    # Split the uri by '/' and get the last part
    parts = uri.split("/")
    return parts[-1]


@retry(when=retry.when.status(429), stop=retry.stop.after_attempt(5))
class FileClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, "/nifile/v1/")

    @get("")
    def api_info(self) -> models.V1Operations:
        """Get information about available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    @get(
        "service-groups/Default/files",
        args=[
            Query,
            Query,
            Query(name="orderBy"),
            Query(name="orderByDescending"),
            Query(name="id"),
        ],
    )
    def __get_files(
        self,
        skip: int = 0,
        take: int = 0,
        order_by: Optional[str] = None,
        order_by_descending: Optional[str] = "false",
        ids: Optional[str] = None,
    ) -> models.FileQueryResponse:
        """Lists available files on the SystemLink File service.
        Use the skip and take parameters to return paged responses.
        The orderBy and orderByDescending fields can be used to manage sorting the list by metadata objects.

        Args:
            skip: How many files to skip in the result when paging. Defaults to 0.
            take: How many files to return in the result, or 0 to use a default defined by the service.
              Defaults to 0.
            order_by: The name of the metadata key to sort by. Defaults to None.
            order_by_descending: The elements in the list are sorted ascending if "false"
              and descending if "true". Defaults to "false".
            ids: Comma-separated list of file IDs to search by. Defaults to None.

        Returns:
            File Query Response

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    def get_files(
        self,
        skip: int = 0,
        take: int = 0,
        order_by: Optional[models.FileQueryOrderBy] = None,
        order_by_descending: Optional[bool] = False,
        ids: Optional[List[str]] = None,
    ) -> models.FileQueryResponse:
        """Lists available files on the SystemLink File service.
        Use the skip and take parameters to return paged responses.
        The orderBy and orderByDescending fields can be used to manage sorting the list by metadata objects.

        Args:
            skip: How many files to skip in the result when paging. Defaults to 0.
            take: How many files to return in the result, or 0 to use a default defined by the service.
            Defaults to 0.
            order_by: The name of the metadata key to sort by. Defaults to None.
            order_by_descending: The elements in the list are sorted ascending if False
            and descending if True. Defaults to False.
            ids: List of file IDs to search by. Defaults to None.

        Returns:
            File Query Response

        Raises:
            ApiException: if unable to communicate with the File Service.
        """
        # Uplink does not support enum serializing into str
        # workaround as the service expects lower case `true` and `false`
        # uplink serializes bools to `True` and `False`
        order_by_str = order_by.value if order_by is not None else None
        order_by_desc_str = "true" if order_by_descending else "false"

        if ids:
            ids_str = ",".join(ids)
        else:
            ids_str = ""

        resp = self.__get_files(
            skip=skip,
            take=take,
            order_by=order_by_str,
            order_by_descending=order_by_desc_str,
            ids=ids_str,
        )

        return resp

    @params({"force": True})  # type: ignore
    @delete("service-groups/Default/files/{id}", args=[Path])
    def delete_file(self, id: str) -> None:
        """Deletes the file indicated by the `file_id`.

        Args:
            id: The ID of the file.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    @params({"force": True})  # type: ignore
    @post("service-groups/Default/delete-files", args=[Field])
    def delete_files(self, ids: List[str]) -> None:
        """Delete multiple files.

        Args:
            ids: List of unique IDs of Files.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    @params({"inline": True})  # type: ignore
    @response_handler(file_like_response_handler)
    @get("service-groups/Default/files/{id}/data", args=[Path])
    def download_file(self, id: str) -> IteratorFileLike:
        """Downloads a file from the SystemLink File service.

        Args:
            id: The ID of the file.

        Yields:
            A file-like object for reading the exported data.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    @response_handler(_file_uri_response_handler)
    @post("service-groups/Default/upload-files")
    def __upload_file(
        self,
        file: Part,
        metadata: Part = None,
        id: Part = None,
        workspace: Query = None,
    ) -> str:
        """Uploads a file using multipart/form-data headers to send the file payload in the HTTP body.

        Args:
            file: The file to upload.
            metadata: JSON Dictionary with key/value pairs
            id: Specify an unique (among all file) 24-digit Hex string ID of the file once it is uploaded.
                Defaults to None.
            workspace: The id of the workspace the file belongs to. Defaults to None.

        Returns:
            ID of uploaded file.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    def upload_file(
        self,
        file: BinaryIO,
        metadata: Optional[Dict[str, str]] = None,
        id: Optional[str] = None,
        workspace: Optional[str] = None,
    ) -> str:
        """Uploads a file to the File Service.

        Args:
            file: The file to upload.
            metadata: File Metadata as dictionary.
            id: Specify an unique (among all file) 24-digit Hex string ID of the file once it is uploaded.
                Defaults to None.
            workspace: The id of the workspace the file belongs to. Defaults to None.

        Returns:
            ID of uploaded file.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """
        if metadata:
            metadata_str = json.dumps(metadata)
        else:
            metadata_str = None

        file_id = self.__upload_file(
            file=file,
            metadata=metadata_str,
            id=id,
            workspace=workspace,
        )

        return file_id

    @post("service-groups/Default/files/{id}/update-metadata", args=[Body, Path])
    def update_metadata(self, metadata: models.UpdateMetadataRequest, id: str) -> None:
        """Updates an existing file's metadata with the specified metadata properties.

        Args:
            metadata: File's metadata and options for updating it.
            id: ID of the file to update Metadata.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """
