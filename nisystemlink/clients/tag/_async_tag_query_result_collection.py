# -*- coding: utf-8 -*-

"""Implementation of AsyncTagQueryResultCollection."""

import abc
from typing import List, Optional

from nisystemlink.clients import core, tag as tbase


class AsyncTagQueryResultCollection(abc.ABC):
    """Represents a paginated list of tags returned by an asynchronous query."""

    def __init__(
        self, first_page: List[tbase.TagData], total_count: int, skip: int
    ) -> None:
        """Initialize an instance with the first page of query results.

        Args:
            first_page: The first page of results, or None if there are no results.
            total_count: The total number of results in the query.
            skip: The skip used for the first page of results.
        """
        self._total_count = total_count
        self._current_page = None  # type: Optional[List[tbase.TagData]]
        if first_page:
            if skip >= total_count:
                raise core.ApiException(
                    "skip is >= totalCount, but the tag list isn't empty"
                )
            self._current_page = first_page
        else:
            pass  # leave it as None, even if passed in as []
        self._skip = skip
        self._current_skip = skip

    @property
    def current_page(self) -> Optional[List[tbase.TagData]]:  # noqa: D401
        """The current page of tag results that were last retrieved from the server, or
        None if there are no more results.

        Use :meth:`move_next_page_async()` to get the next page of results.
        """
        return self._current_page

    @property
    def total_count(self) -> int:  # noqa: D401
        """The total number of tags matched by the query at the time the query was made."""
        return self._total_count

    async def move_next_page_async(self) -> Optional[List[tbase.TagData]]:
        """Asynchronously retrieve the next page of query results from the server,
        returning them and updating :attr:`current_page`.

        Does nothing if the last page has already been retrieved. Use
        :meth:`reset_async()` to start again from the first page.

        Returns:
            A task representing the asynchronous operation. On success, contains the
            next page of results, or None if there are no more results.

        Raises:
            ApiException: if the API call fails.
        """
        if self._current_page is None:
            return None

        new_skip = self._current_skip + len(self._current_page)
        if new_skip < self.total_count:
            self._current_page = await self._query_page_async(new_skip)
        else:
            self._current_page = None

        self._current_skip = new_skip
        return self._current_page

    async def reset_async(self) -> List[tbase.TagData]:
        """Asynchronously query the server for a fresh set of results, returning the
        first page and updating :attr:`current_page` and :attr:`total_count`.

        Returns:
            A task representing the asynchronous operation. On success, contains the
            first page of results, or None if there are no results.

        Raises:
            ApiException: if the API call fails.
        """
        self._current_skip = self._skip
        self._current_page = await self._query_page_async(self._current_skip)
        return self._current_page

    @abc.abstractmethod
    async def _query_page_async(self, skip: int) -> List[tbase.TagData]:
        """Asynchronously query for a single page of results and updates :attr:`total_count`.

        Args:
            skip: The skip to use in the query.

        Returns:
            A task representing the asynchronous operation. On completion, the page of
            results, or None if there are no more results.

        Raises:
            ApiException: if the API call fails.
        """
        ...
