# -*- coding: utf-8 -*-

"""Implementation of TagQueryResultCollection."""

import abc
from typing import Iterable, List, Optional

from nisystemlink.clients import core, tag as tbase


class TagQueryResultCollection(abc.ABC):
    """Represents a paginated list of tags returned by a query.

    Iterating over the collection makes additional server requests to retrieve pages
    after the first.
    """

    def __init__(
        self, first_page: List[tbase.TagData], total_count: int, skip: int
    ) -> None:
        """Initialize an instance with the first page of query results.

        Args:
            first_page: The first page of results, or None if there are no results.
            total_count: The total number of results in the query.
            skip: The skip used for the first page of results.
        """
        self._first_page = None  # type: Optional[List[tbase.TagData]]
        if first_page:
            if skip >= total_count:
                raise core.ApiException(
                    "skip is >= totalCount, but the tag list isn't empty"
                )
            self._first_page = first_page
        else:
            pass  # leave it as None, even if passed in as []
        self._use_cached_page = True
        self._total_count = total_count
        self._skip = skip

    @property
    def total_count(self) -> int:  # noqa: D401
        """The total number of tags matched by the query at the time the query was made."""
        return self._total_count

    def __iter__(self) -> Iterable[List[tbase.TagData]]:
        """Enumerate over the pages of tag query results.

        Calls to ``next(iter())`` may throw :class:`.ApiException`.

        Returns:
            The created enumerator.
        """
        skip = self._skip

        if self._use_cached_page:
            self._use_cached_page = False
            page = self._first_page
            self._first_page = None

            if not page:
                return

            skip += len(page)
            yield page

            if skip >= self._total_count:
                return

        while True:
            page = self._query_page(skip)

            if not page:
                return

            skip += len(page)
            yield page

            if skip >= self._total_count:
                break

    @abc.abstractmethod
    def _query_page(self, skip: int) -> List[tbase.TagData]:
        """Query for a single page of results and updates :attr:`total_count`.

        Args:
            skip: The skip to use in the query.

        Returns:
            The page of results, or None if there are no more results.

        Raises:
            ApiException: if the API call fails.
        """
        ...
