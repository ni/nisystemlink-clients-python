"""Implementation of FileClient."""

from typing import Literal, Optional

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
from uplink import Body, Path, Query

from . import models


def _iter_content_filelike_wrapper(response: Response) -> IteratorFileLike:
    return IteratorFileLike(response.iter_content(chunk_size=4096))


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
        order_by: Optional[
            Literal["created", "id", "size", "lastUpdatedTimestamp"]
        ] = None,
        order_by_descending: Optional[Literal["true", "false"]] = "false",
        file_ids: Optional[str] = None,
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
            file_ids: Comma-separated list of file IDs to search by. Defaults to None.

        Returns:
            File Query Response

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    def get_files(
        self,
        skip: int = 0,
        take: int = 0,
        order_by: Optional[
            Literal["created", "id", "size", "lastUpdatedTimestamp"]
        ] = None,
        order_by_descending: Optional[bool] = False,
        file_ids: Optional[str] = None,
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
            file_ids: Comma-separated list of file IDs to search by. Defaults to None.

        Returns:
            File Query Response

        Raises:
            ApiException: if unable to communicate with the File Service.
        """
        # wrapper workaround as the service expects lower case `true` and `false`
        # uplink serializes bools to `True` and `False`
        if order_by_descending:
            resp = self.__get_files(
                skip=skip,
                take=take,
                order_by=order_by,
                order_by_descending="true",
                file_ids=file_ids,
            )
        else:
            resp = self.__get_files(
                skip=skip,
                take=take,
                order_by=order_by,
                order_by_descending="false",
                file_ids=file_ids,
            )

        return resp

    @delete("service-groups/Default/files/{file_id}", args=[Path, Query])
    def delete_file(self, file_id: str, force: bool = False) -> None:
        """Deletes the file indicated by the `file_id`.

        Args:
            file_id: The ID of the file.
            force: Whether the deletion of a file will be forced. Defaults to False.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    @post("service-groups/Default/delete-files", args=[Body, Query])
    def delete_files(
        self, files: models.DeleteMutipleRequest, force: bool = False
    ) -> None:
        """Delete multiple files.

        Args:
            files: The description of files to delete.
            force: Whether the deletion of files will be forced. Defaults to False.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """

    # TBD: Error with poe types - Untyped decorator makes function "download_file" untyped
    # @params({"inline": True})
    @response_handler(_iter_content_filelike_wrapper)
    @get("service-groups/Default/files/{file_id}/data", args=[Path, Query])
    def download_file(self, file_id: str, inline: bool = True) -> IteratorFileLike:
        """Downloads a file from the SystemLink File service.

        Args:
            file_id: The ID of the file.
            inline: Return the file inline. Defaults to True.

        Yields:
            A file-like object for reading the exported data.

        Raises:
            ApiException: if unable to communicate with the File Service.
        """
