# -*- coding: utf-8 -*-

"""Implementation of TemporaryTagSelection."""

from types import TracebackType
from typing import Awaitable, List, Optional, Type

from nisystemlink.clients import core, tag as tbase
from nisystemlink.clients.core._internal._http_client import HttpClient
from typing_extensions import final


@final
class TemporaryTagSelection:
    """Manages the lifetime of short-lived tag selections that are used within a single API call.

    Closing the instance deletes the selection.
    """

    _TEMPORARY_SELECTION_TIMEOUT_SECONDS = 30
    """Inactivity timeout for short-lived selections created within a single API call."""

    __MAGIC = object()

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'TemporaryTagSelection' is not an acceptable base type")

    @classmethod
    def create(cls, client: HttpClient, paths: List[str]) -> "TemporaryTagSelection":
        """Create a temporary tag selection containing the given paths.

        Args:
            client: The HTTP client object for communicating with the server.
            paths: The tag search paths to include in the selection.
        """
        selection = TemporaryTagSelection(cls.__MAGIC, client)
        selection._create(paths)
        return selection

    @classmethod
    async def create_async(
        cls, client: HttpClient, paths: List[str]
    ) -> "TemporaryTagSelection":
        """Asynchronously create a temporary tag selection containing the given paths.

        Args:
            client: The HTTP client object for communicating with the server.
            paths: The tag search paths to include in the selection.

        Returns:
            A task representing the asynchronous operation. On completion, contains the
            created selection.
        """
        selection = TemporaryTagSelection(cls.__MAGIC, client)
        await selection._create_async(paths)
        return selection

    def __init__(self, magic: object, client: HttpClient) -> None:
        assert (
            magic == self.__MAGIC
        ), "Do not construct a TemporaryTagSelection directly. Use create() instead."
        self._api = client.at_uri("/nitag/v2/selections")
        self._id = None  # type: Optional[str]

    @property
    def id(self) -> Optional[str]:  # noqa: D401
        """The ID of the selection."""
        return self._id

    def close(self) -> None:
        """Close the selection."""
        if self._id is None:
            return

        try:
            self._api.delete("/{id}", params={"id": self._id})
        except core.ApiException:
            pass

        self._id = None

    async def close_async(self) -> None:
        """Asynchronously close the selection.

        Returns:
            A task representing the asynchronous operation.
        """
        if self._id is None:
            return

        try:
            await self._api.as_async.delete("/{id}", params={"id": self._id})
        except core.ApiException:
            pass

        self._id = None

    def __enter__(self) -> "TemporaryTagSelection":
        return self

    async def __aenter__(self) -> "TemporaryTagSelection":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Awaitable[None]:
        return self.close_async()

    def __del__(self) -> None:
        self.close()

    def _create(self, paths: List[str]) -> None:
        selection, http_response = self._api.post(
            "",
            data={
                "searchPaths": paths,
                "inactivityTimeout": self._TEMPORARY_SELECTION_TIMEOUT_SECONDS,
            },
        )

        if selection is None or selection.get("id") is None:
            raise tbase.TagManager.invalid_response(http_response)

        self._id = selection["id"]

    async def _create_async(self, paths: List[str]) -> None:
        selection, http_response = await self._api.as_async.post(
            "",
            data={
                "searchPaths": paths,
                "inactivityTimeout": self._TEMPORARY_SELECTION_TIMEOUT_SECONDS,
            },
        )

        if selection is None or selection.get("id") is None:
            raise tbase.TagManager.invalid_response(http_response)

        self._id = selection["id"]
