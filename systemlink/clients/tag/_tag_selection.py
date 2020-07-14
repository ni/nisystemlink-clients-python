# -*- coding: utf-8 -*-

"""Implementation of TagSelection."""

import abc
import asyncio
import datetime
from types import TracebackType
from typing import Awaitable, Dict, List, Optional, Sequence, Tuple, Type, Union

from systemlink.clients import tag as tbase
from systemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)


class TagSelection(tbase.ITagReader):
    """Represents a set of tags that can be read, written, or deleted together.

    Tags may be specified using glob-style wildcards to include multiple tags with a
    common path. Call :meth:`close()` to free resources. Tag reads are buffered, and the
    latest values are only retrieved on first read or by calling
    :meth:`refresh_values()`. Reads for tags that aren't in the selection return None,
    even if the tag exists on the server.

    Note that :class:`TagSelection` objects support using the ``with`` statement (or the
    ``async with`` statement), to :meth:`close()` the selection automatically on exit.
    """

    def __init__(
        self, tags: Sequence[tbase.TagData], paths: Optional[Sequence[str]] = None
    ) -> None:
        """Initialize a selection using queried or existing tag data.

        Args:
            tags: The tags to store in the selection.
            paths: The paths used to query the tags. If left as None, the paths will be
                extracted from ``tags``.

        Raises:
            ValueError: if ``tags`` is None or empty.
            ValueError: if ``tags`` or ``paths`` contains duplicate tags.
        """
        if tags is None:
            raise ValueError("tags cannot be None")
        if any(t is None for t in tags):
            raise ValueError("tags cannot contain None")
        if any(not t.path for t in tags):
            raise ValueError("tags cannot contain a tag with an empty path")

        self._metadata = {m.path: m for m in tags}
        if len(self._metadata) != len(tags):
            raise ValueError("tags contains duplicate paths")

        if paths is None:
            self._paths = set(self._metadata.keys())
        else:
            if any(p is None for p in paths):
                raise ValueError("paths cannot contain None")
            self._paths = set(paths)
            if len(self._paths) != len(paths):
                raise ValueError("paths contains duplicates")

        self._readers = {
            r.path: r
            for r in (self._create_value_reader(m) for m in self._metadata.values())
            if r is not None
        }

        self._values = None  # type: Optional[Dict[str, SerializedTagWithAggregates]]

        self._closed = False

    @property
    def paths(self) -> Tuple[str, ...]:  # noqa: D401
        """The paths of all tags in the selection, including those that do not exist on the server.

        When using wildcards, the original paths with the wildcards are included in the
        list, not the paths matched by the wildcards.
        """
        return tuple(self._paths)

    @property
    def metadata(self) -> Dict[str, tbase.TagData]:  # noqa: D401
        """The most recently retrieved metadata for tags in the selection, indexed by :attr:`TagData.path`.

        Tags in the selection that do not exist on the server will not appear in the
        collection. Call :meth:`refresh_metadata()` to update the data contained in the
        collection.
        """
        return dict(self._metadata)

    @property
    def values(self) -> Dict[str, tbase.TagValueReader]:  # noqa: D401
        """A :class:`.TagValueReader` for reading the most recently retrieved value for
        tags in the selection, indexed by :attr:`.TagValueReader.path`.

        Tags in the selection that do not exist on the server will not appear in the
        collection. Readers for tags without values on the server will return None when
        read. Call :meth:`refresh_values()` to update the values returned by the readers
        in the dictionary.
        """
        return dict(self._readers)

    @abc.abstractmethod
    def _close_internal(self) -> None:
        """Clean up server resources associated with the selection."""
        ...

    @abc.abstractmethod
    async def _close_internal_async(self) -> None:
        """Asynchronously clean up server resources associated with the selection.

        Returns:
            A task representing the asynchronous operation.
        """
        ...

    @abc.abstractmethod
    def _create_subscription_internal(
        self, update_interval: Optional[datetime.timedelta] = None
    ) -> tbase.TagSubscription:
        """Subscribe to receive events when tags in the selection are written to using the specified update interval.

        Args:
            update_interval: How often to receive tag update notifications from the
                server, or None to use the default.

        Returns:
            The created subscription.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _create_subscription_internal_async(
        self, update_interval: Optional[datetime.timedelta] = None
    ) -> tbase.TagSubscription:
        """Asynchronously subscribe to receive events when tags in the selection are
        written to using the specified update interval.

        Args:
            update_interval: How often to receive tag update notifications from the
                server, or None to use the default.

        Returns:
            A task representing the asynchronous operation. On success, contains the
            created subscription.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    def _delete_tags_from_server_internal(self) -> None:
        """Delete all tags in the selection from the server.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _delete_tags_from_server_internal_async(self) -> None:
        """Asynchronously delete all tags in the selection from the server.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    def _read_tag_metadata(self) -> List[tbase.TagData]:
        """Retrieve the metadata of all tags in the selection.

        Returns:
            The list of tag metadata.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    def _read_tag_values(self) -> List[Optional[SerializedTagWithAggregates]]:
        """Retrieve the values of all tags in the selection.

        Returns:
            The list of the tag values.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    def _read_tag_metadata_and_values(
        self,
    ) -> Tuple[List[tbase.TagData], List[Optional[SerializedTagWithAggregates]]]:
        """Retrieve the metadata and values of all tags in the selection.

        Returns:
            A tuple with the list of tag metadata and the list of tag values.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _read_tag_metadata_async(self) -> List[tbase.TagData]:
        """Asynchronously retrieve the metadata of all tags in the selection.

        Returns:
            A task representing the asynchronous operation. When complete, contains the
            list of tag metadata.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _read_tag_values_async(
        self,
    ) -> List[Optional[SerializedTagWithAggregates]]:
        """Asynchronously retrieve the values of all tags in the selection.

        Returns:
            A task representing the asynchronous operation. When complete, contains the
            list of the tag values.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _read_tag_metadata_and_values_async(
        self,
    ) -> Tuple[List[tbase.TagData], List[Optional[SerializedTagWithAggregates]]]:
        """Asynchronously retrieve the metadata and values of all tags in the selection.

        Returns:
            A task representing the asynchronous operation. When complete, contains a
            tuple with the list of tag metadata and the list of tag values.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    def _reset_aggregates_internal(self) -> None:
        """Reset the aggregate values of tags in the selection.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _reset_aggregates_internal_async(self) -> None:
        """Asynchronously reset the aggregate values of tags in the selection.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ApiException: if the API call fails.
        """
        ...

    def _on_paths_changed(self) -> None:
        """Note when the contents of :attr:`paths` is modified.

        The default implementation does nothing.
        """
        pass

    def add_tags(self, tags: List[tbase.TagData]) -> None:
        """Add one or more tags to the selection.

        Tags that are already in the selection are ignored. The tags as given are
        immediately available in the :attr:`metadata` collection. Use
        :meth:`refresh_metadata()` to get the latest data for the tags. The tags will be
        available in the :attr:`values` collection but won't have latest a latest value
        until :meth:`refresh_values()` is called.

        Args:
            tags: The tags to add to the selection.

        Raises:
            ValueError: if any of the given tags are None or have an invalid path.
            ValueError: if ``tags`` is None.
            ReferenceError: if the selection has been closed.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        for tag in self._validate_tags(tags):
            self._paths.add(tag.path)

            # Don't overwrite existing.
            if tag.path not in self._metadata:
                self._metadata[tag.path] = tag
                reader = self._create_value_reader(tag)
                if reader is not None:
                    self._readers[tag.path] = reader

        self._on_paths_changed()

    def clear_tags(self) -> None:
        """Remove all tags from the selection.

        Raises:
            ReferenceError: if the selection has been closed.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        self._paths.clear()
        self._metadata.clear()
        self._readers.clear()

        self._on_paths_changed()

    def close(self) -> None:
        """Clean up server resources associated with the selection."""
        if self._closed:
            return

        self._close_internal()
        self._closed = True
        self._paths.clear()
        self._metadata.clear()
        self._readers.clear()
        if self._values is not None:
            self._values.clear()

    async def close_async(self) -> None:
        """Asynchronously clean up server resources associated with the selection.

        Returns:
            A task representing the asynchronous operation.
        """
        if self._closed:
            return

        await self._close_internal_async()
        self._closed = True
        self._paths.clear()
        self._metadata.clear()
        self._readers.clear()
        if self._values is not None:
            self._values.clear()

    def create_subscription(
        self, *, update_interval: Optional[datetime.timedelta] = None
    ) -> tbase.TagSubscription:
        """Subscribe to receive events when tags in the selection are written to.

        Updates will be queried from the server using the specified or default update
        interval.

        The subscription will include any tags that are currently included in the
        selection when the subscription is created. That list can be seen via the
        :attr:`metadata` property. The subscription will also attempt to include any
        non-wildcard paths that are in the selection's current list of :attr:`paths`.
        Often, the list of :attr:`paths` directly coincides with the :attr:`metadata`,
        but the former may contain paths that did not exist when the selection's
        metadata was last updated from the server, e.g. via :meth:`refresh()`.

        Closing, adding tags, or removing tags from the selection will not affect
        previously created subscriptions.

        Args:
            update_interval: How often to receive tag updates notifications from the
                server. Default is ``datetime.timedelta(seconds=30)``.

        Returns:
            The created subscription.

        Raises:
            ValueError: if update_interval is negative.
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        if update_interval is not None and update_interval.total_seconds() < 0:
            raise ValueError("update_interval cannot be negative")

        return self._create_subscription_internal(update_interval)

    def create_subscription_async(
        self, *, update_interval: Optional[datetime.timedelta] = None
    ) -> Awaitable[tbase.TagSubscription]:
        """Asynchronously subscribe to receive events when tags in the selection are written to.

        Updates will be queried from the server using the specified or default update
        interval.

        Closing, adding tags, or removing tags from the selection will not affect
        previously created subscriptions.

        Args:
            update_interval: How often to receive tag updates notifications from the
                server. Depending on the :class:`TagManager` implementation in use, this
                may involve polling the server or have a minimum value.

        Returns:
            A task representing the asynchronous operation. On success, contains the
            created subscription.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            f = asyncio.get_event_loop().create_future()
            f.set_exception(ReferenceError("TagSelection"))
            return f

        if update_interval and update_interval.total_seconds() < 0:
            f = asyncio.get_event_loop().create_future()
            f.set_exception(ValueError("update_interval cannot be negative"))
            return f

        return self._create_subscription_internal_async(update_interval)

    def delete_tags_from_server(self) -> None:
        """Delete all tags in the selection from the server.

        The tags are not removed from the selection but are removed from
        :attr:`metadata` and :attr:`values`. If any of the tags are recreated, a call to
        :meth:`refresh_metadata()` will restore them in the collection of tags.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        self._delete_tags_from_server_internal()
        self._metadata.clear()
        self._readers.clear()
        if self._values is not None:
            self._values.clear()

    async def delete_tags_from_server_async(self) -> None:
        """Asynchronously delete all tags in the selection from the server.

        The tags are not removed from the selection but are removed from
        :attr:`metadata` and :attr:`values`. If any of the tags are recreated, a call to
        :meth:`refresh_metadata()` will restore them in the collection of tags.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        await self._delete_tags_from_server_internal_async()
        self._metadata.clear()
        self._readers.clear()
        if self._values is not None:
            self._values.clear()

    def open_tags(self, paths: List[str]) -> None:
        """Add one or more tags to the selection by path.

        Tags that are already in the selection are ignored. The tags will not be
        available in the :attr:`metadata` collection until :meth:`refresh_metadata()` is
        called or the :attr:`values` collection until :meth:`refresh_values()` is
        called.

        Args:
            paths: The tag paths to add to the selection. May include glob-style
                wildcards.

        Raises:
            ValueError: if any of the given paths are None or invalid.
            ValueError: if ``paths`` is None.
            ReferenceError: if the selection has been closed.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        self._paths.update(self._validate_paths(paths))
        self._on_paths_changed()

    def refresh(self) -> None:
        """Refresh both :class:`TagData` and current values for all tags in the
        selection, updating :attr:`metadata` and :attr:`values` accordingly.

        Call :meth:`refresh_metadata()` or :meth:`refresh_values()` to only partially
        refresh.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        (metadata, values) = self._read_tag_metadata_and_values()
        self._update_metadata(metadata)
        self._update_values(values)

    async def refresh_async(self) -> None:
        """Asynchronously refresh both the :class:`TagData` and current values for all
        tags in the selection, updating :attr:`metadata` and :attr:`values` accordingly.

        Call :meth:`refresh_metadata_async()` or :meth:`refresh_values_async()` to only
        partially refresh.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        (metadata, values) = await self._read_tag_metadata_and_values_async()
        self._update_metadata(metadata)
        self._update_values(values)

    def refresh_metadata(self) -> None:
        """Refresh the :class:`TagData` for all tags in the selection, updating :attr:`metadata` accordingly.

        :attr:`values` will also be updated with new and removed tags, but those readers
        will continue to return previously available values until
        :meth:`refresh_values()` is called.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        metadata = self._read_tag_metadata()
        self._update_metadata(metadata)

    async def refresh_metadata_async(self) -> None:
        """Asynchronously refresh the :class:`TagData` for all tags in the selection,
        updating :attr:`metadata` accordingly.

        :attr:`values` will also be updated with new and removed tags, but those readers
        will continue to return previously available values until
        :meth:`refresh_values()` is called.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        metadata = await self._read_tag_metadata_async()
        self._update_metadata(metadata)

    def refresh_values(self) -> None:
        """Refresh the current value of tags in the selection returned by the readers in the :attr:`values` collection.

        Readers will return None for tags that no longer exist on the server, or exist
        but haven't yet been written to. New readers will be added to the collection for
        tags that have values but have not yet been added to :attr:`metadata` by a call
        to :meth:`refresh_metadata()`.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        values = self._read_tag_values()
        self._update_values(values)

    async def refresh_values_async(self) -> None:
        """Asynchronously refresh the current value of tags in the selection returned by
        the readers in the :attr:`values` collection.

        Readers will return None for tags that no longer exist on the server, or exist
        but haven't yet been written to. New readers will be added to the collection for
        tags that have values but have not yet been added to :attr:`metadata` by a call
        to :meth:`refresh_metadata()`.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        values = await self._read_tag_values_async()
        self._update_values(values)

    def remove_tags(self, tags: List[Union[tbase.TagData, str]]) -> None:
        """Remove one or more tags from the selection.

        The tags are not removed from the :attr:`metadata` and :attr:`values`
        collections until the next :meth:`refresh_metadata()`.

        Tags not in the selection are ignored. Tags that were added to the selection
        using wildcard paths can only be removed by including the same wildcard paths.
        Tags matched by multiple wildcard paths remain in the selection until all of the
        paths are removed.

        Args:
            tags: The tags to remove from the selection. Either strings (paths) or
                :class:`TagData` objects can be given. For :class:`TagData` objects,
                only the :attr:`TagData.path` is used.

        Raises:
            ValueError: if ``tags`` is None.
            ValueError: if any of the given tags are None or have an invalid path.
            ReferenceError: if the selection has been closed.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        if tags is None:
            raise ValueError("tags cannot be None")

        paths = [t for t in tags if isinstance(t, str)]
        tags_ = [t for t in tags if not isinstance(t, str)]

        self._paths.difference_update(self._validate_paths(paths))
        self._paths.difference_update(t.path for t in self._validate_tags(tags_))

        self._on_paths_changed()

    def reset_aggregates(self) -> None:
        """Reset tag value aggregates on the server for all tags in the selection.

        Tag historical values are not modified. Has no effect on tags that are not set
        to :attr:`TagData.collect_aggregates`. Use :meth:`refresh_values()` to retrieve
        the new aggregates.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            raise ReferenceError("TagSelection")

        self._reset_aggregates_internal()

    def reset_aggregates_async(self) -> Awaitable[None]:
        """Asynchronously reset tag value aggregates on the server for all tags in the selection.

        Tag historical values are not modified. Has no effect on tags that are not set
        to :attr:`TagData.collect_aggregates`. Use :meth:`refresh_values()` to retrieve
        the new aggregates.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ReferenceError: if the selection has been closed.
            ApiException: if the API call fails.
        """
        if self._closed:
            f = asyncio.get_event_loop().create_future()
            f.set_exception(ReferenceError("TagSelection"))
            return f

        return self._reset_aggregates_internal_async()

    def __enter__(self) -> "TagSelection":
        return self

    async def __aenter__(self) -> "TagSelection":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Clean up resources associated with the selection."""
        self.close()

    def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Awaitable[None]:
        """Asynchronously clean up resources associated with the selection."""
        return self.close_async()

    def __del__(self) -> None:
        """Finalize resources associated with the selection."""
        self.close()

    def _read(
        self, path: str, include_timestamp: bool, include_aggregates: bool
    ) -> Optional[Optional[SerializedTagWithAggregates]]:
        if self._closed:
            raise ReferenceError("TagSelection")

        if path is None:
            raise ValueError("path cannot be None")

        if self._values is None:
            self.refresh_values()
            assert self._values is not None

        if path in self._values:
            return self._values[path]
        elif path in self._readers:
            return None
        else:
            raise ValueError("Cannot read a tag that is not in the selection")

    async def _read_async(
        self, path: str, include_timestamp: bool, include_aggregates: bool
    ) -> Optional[Optional[SerializedTagWithAggregates]]:
        if self._closed:
            raise ReferenceError("TagSelection")

        if path is None:
            raise ValueError("path cannot be None")

        if self._values is None:
            await self.refresh_values_async()
            assert self._values is not None

        if path in self._values:
            return self._values[path]
        elif path in self._readers:
            return None
        else:
            raise ValueError("Cannot read a tag that is not in the selection")

    def _create_value_reader(
        self, tag: tbase.TagData
    ) -> Optional[tbase.TagValueReader]:
        if tag is None:
            raise ValueError("tag cannot be None")

        if tag.data_type == tbase.DataType.UNKNOWN:
            return None
        else:
            return tbase.TagValueReader(self, tag)

    def _update_metadata(self, metadata: List[tbase.TagData]) -> None:
        missing_paths = set(self._metadata.keys()).difference(t.path for t in metadata)
        for missing_path in missing_paths:
            del self._metadata[missing_path]
            if missing_path in self._readers:
                del self._readers[missing_path]
            if self._values is not None and missing_path in self._values:
                del self._values[missing_path]

        for tag in metadata:
            old_tag = self._metadata.get(tag.path)
            if old_tag is None or old_tag.data_type != tag.data_type:
                reader = self._create_value_reader(tag)
                if reader is not None:
                    self._readers[tag.path] = reader

            self._metadata[tag.path] = tag

    def _update_values(
        self, values: List[Optional[SerializedTagWithAggregates]]
    ) -> None:
        if self._values is None:
            self._values = {}

        missing_values = set(self._values.keys()).difference(
            v.path for v in values if v is not None
        )
        for missing_path in missing_values:
            del self._values[missing_path]

        for value in values:
            if value is None:
                continue

            self._values[value.path] = value

            tag = self._metadata.get(value.path)
            if tag is None:
                tag = tbase.TagData(value.path, value.data_type)
                self._metadata[value.path] = tag
            elif tag.data_type != value.data_type:
                tag.data_type = value.data_type
            else:
                continue

            reader = self._create_value_reader(tag)
            if reader is not None:
                self._readers[value.path] = reader

    @classmethod
    def _validate_paths(cls, paths: List[str]) -> List[str]:
        """Validate that the given tag paths are valid for queries.

        Args:
            paths: The paths to validate.

        Returns:
            The validated paths.

        Raises:
            ValueError: if any of the given paths are None or invalid.
            ValueError: if ``paths`` is None.
        """
        ...
        if paths is None:
            raise ValueError("paths cannot be None")

        for path in paths:
            if path is None:
                raise ValueError("paths cannot contain None")
            tbase.TagPathUtilities.validate_query(path)

        return paths

    @classmethod
    def _validate_tags(cls, tags: List[tbase.TagData]) -> List[tbase.TagData]:
        """Validate that the given tags have valid paths.

        Args:
            tags: The tags to validate.

        Returns:
            The validated tags.

        Raises:
            ValueError: if any of the given tags are None or have an invalid path.
            ValueError: if ``tags`` is None.
        """
        ...
        if tags is None:
            raise ValueError("tags cannot be None")

        for tag in tags:
            if tag is None:
                raise ValueError("tags cannot contain None")
            tag.validate_path()

        return tags
