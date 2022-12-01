# -*- coding: utf-8 -*-

"""Implementation of TagManager."""

import asyncio
import datetime
from typing import (
    Any,
    Awaitable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from nisystemlink.clients import core, tag as tbase
from nisystemlink.clients.core._internal._http_client import HttpClient, HttpResponse
from nisystemlink.clients.core._internal._timestamp_utilities import TimestampUtilities
from nisystemlink.clients.tag._core._manual_reset_timer import ManualResetTimer
from nisystemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)
from nisystemlink.clients.tag._core._system_time_stamper import SystemTimeStamper
from nisystemlink.clients.tag._http._http_async_tag_query_result_collection import (
    HttpAsyncTagQueryResultCollection,
)
from nisystemlink.clients.tag._http._http_buffered_tag_writer import (
    HttpBufferedTagWriter,
)
from nisystemlink.clients.tag._http._http_tag_query_result_collection import (
    HttpTagQueryResultCollection,
)
from nisystemlink.clients.tag._http._http_tag_selection import HttpTagSelection
from nisystemlink.clients.tag._http._temporary_tag_selection import (
    TemporaryTagSelection,
)
from typing_extensions import final


@final
class TagManager(tbase.ITagReader):
    """Represents common ways to create, read, and query SystemLink tags for a specific server connection."""

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'TagManager' is not an acceptable base type")

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None) -> None:
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect.

        Raises:
            ApiException: if the current system cannot communicate with a SystemLink
                Server, or if the configuration provided by SystemLink Client cannot be
                found.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        self._http_client = HttpClient(configuration)
        self._api = self._http_client.at_uri("/nitag/v2")

    def create_selection(self, tags: List[tbase.TagData]) -> tbase.TagSelection:
        """Create an :class:`TagSelection` that initially contains the given ``tags``
        without retrieving any additional data from the server.

        Args:
            tags: The tags to include in the selection.

        Returns:
            The created selection.

        Raises:
            ValueError: if any of the given ``tags`` is None or has an invalid path.
            ValueError: if ``tags`` is None.
        """
        return HttpTagSelection(self._http_client, tags)

    def open_selection(self, paths: List[str]) -> tbase.TagSelection:
        """Query the server for the metadata for the given tag ``paths`` and return the
        results in a :class:`TagSelection`.

        Args:
            paths: The paths of the tags to include in the selection. May include
                glob-style wildcards.

        Returns:
            The created selection with :attr:`TagSelection.metadata` containing the
            metadata.

        Raises:
            ValueError: if any of the given ``paths`` is None or invalid.
            ValueError: if ``paths`` contains duplicate paths.
            ValueError: if ``paths`` is None.
            ApiException: if the API call fails.
        """
        return HttpTagSelection.open(self._http_client, paths)

    def open_selection_async(self, paths: List[str]) -> Awaitable[tbase.TagSelection]:
        """Asynchronously query the server for the metadata for the given tag ``paths``
        and return the results in a :class:`TagSelection`.

        Args:
            paths: The paths of the tags to include in the selection. May include
                glob-style wildcards.

        Returns:
            A task representing the asynchronous operation. On success, contains the
            created selection with :attr:`TagSelection.metadata` containing the
            metadata.

        Raises:
            ValueError: if any of the given ``paths`` is None or invalid.
            ValueError: if ``paths`` contains duplicate paths.
            ValueError: if ``paths`` is None.
            ApiException: if the API call fails.
        """
        return HttpTagSelection.open_async(self._http_client, paths)

    def open(
        self,
        path: str,
        data_type: Optional[tbase.DataType] = None,
        *,
        create: Optional[bool] = None
    ) -> tbase.TagData:
        """Query the server for the metadata of a tag, optionally creating it if it doesn't already exist.

        If ``data_type`` is provided, ``create`` defaults to True. If ``data_type`` is
        not provided, ``create`` cannot be set to True.

        The call fails if the tag already exists as a different data type than specified
        or if it doesn't exist and ``create`` is False.

        Args:
            path: The path of the tag to open.
            data_type: The expected data type of the tag.
            create: True to create the tag if it doesn't already exist, False to fail if
                it doesn't exist.

        Returns:
            Information about the tag.

        Raises:
            ValueError: if ``path`` is None or empty.
            ValueError: if ``data_type`` is invalid.
            ValueError: if ``create`` is True, but ``data_type`` is None.
            ApiException: if the API call fails.
        """
        if create is None:
            create = data_type is not None
        elif create is True:
            if data_type is None:
                raise ValueError("Cannot create if data_type is not specified")

        if data_type == tbase.DataType.UNKNOWN:
            raise ValueError("Must specify a valid data type")

        tag = None  # type: Optional[Dict[str, Any]]
        try:
            tag, _ = self._api.get(
                "/tags/{path}", params={"path": tbase.TagPathUtilities.validate(path)}
            )
        except core.ApiException as ex:
            error_name = None if ex.error is None else ex.error.name
            if create and (error_name or "").startswith("Tag.NoSuchTag"):
                pass  # continue on and create the tag
            else:
                raise

        if tag is not None:
            if data_type is not None and tag["type"] != data_type.api_name:
                raise core.ApiException("Tag exists with a conflicting data type")

            return tbase.TagData.from_json_dict(tag)
        else:
            if data_type is None:
                raise ValueError("data_type cannot be None when create is True")

            # Tag didn't already exist, so try to create it.
            self._api.post("/tags", data={"type": data_type.api_name, "path": path})
            return tbase.TagData(path, data_type)

    async def open_async(
        self,
        path: str,
        data_type: Optional[tbase.DataType] = None,
        *,
        create: Optional[bool] = None
    ) -> tbase.TagData:
        """Asynchronously query the server for the metadata of a tag, optionally
        creating it if it doesn't already exist.

        The call fails if the tag already exists as a different data type than specified
        or if it doesn't exist and ``create`` is False.

        Args:
            path: The path of the tag to open.
            data_type: The expected data type of the tag.
            create: True to create the tag if it doesn't already exist, False to fail if
                it doesn't exist.

        Returns:
            A task representing the asynchronous operation. On success, contains
            information about the tag.

        Raises:
            ValueError: if ``path`` is None or empty.
            ValueError: if ``data_type`` is invalid.
            ValueError: if ``create`` is True, but ``data_type`` is None.
            ApiException: if the API call fails.
        """
        if create is None:
            create = data_type is not None
        elif create is True:
            if data_type is None:
                raise ValueError("Cannot create if data_type is not specified")

        if data_type == tbase.DataType.UNKNOWN:
            raise ValueError("Must specify a valid data type")

        tag = None  # type: Optional[Dict[str, Any]]
        try:
            tag, _ = await self._api.as_async.get(
                "/tags/{path}", params={"path": tbase.TagPathUtilities.validate(path)}
            )
        except core.ApiException as ex:
            error_name = None if ex.error is None else ex.error.name
            if create and (error_name or "").startswith("Tag.NoSuchTag"):
                pass  # continue on and create the tag
            else:
                raise

        if tag is not None:
            if data_type is not None and tag["type"] != data_type.api_name:
                raise core.ApiException("Tag exists with a conflicting data type")

            return tbase.TagData.from_json_dict(tag)
        else:
            if data_type is None:
                raise ValueError("data_type cannot be None when create is True")

            # Tag didn't already exist, so try to create it.
            await self._api.as_async.post(
                "/tags", data={"type": data_type.api_name, "path": path}
            )
            return tbase.TagData(path, data_type)

    def refresh(self, tags: List[tbase.TagData]) -> None:
        """Populate the given ``tags`` with the latest metadata from the server.

        Only the :attr:`TagData.path` needs to be initialized. Tags that don't exist on
        the server will have their :attr:`TagData.data_type` set to
        :attr:`DataType.UNKNOWN`.

        Args:
            tags: The tags to refresh.

        Raises:
            ValueError: if any ``tags`` are None or have invalid paths.
            ValueError: if ``tags`` is None.
            ApiException: if the API call fails.
        """
        paths = self._prepare_refresh(tags)
        response, http_response = self._api.get(
            "/tags", params={"path": paths, "take": str(len(tags))}
        )
        self._handle_refresh(tags, response, http_response)

    async def refresh_async(self, tags: List[tbase.TagData]) -> None:
        """Asynchronously populate the given ``tags`` with the latest metadata from the server.

        Only the :attr:`TagData.path` needs to be initialized. Tags that don't exist on
        the server will have their :attr:`TagData.data_type` set to
        :attr:`DataType.UNKNOWN`.

        Args:
            tags: The tags to refresh.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ValueError: if any ``tags`` are None or have invalid paths.
            ValueError: if ``tags`` is None.
            ApiException: if the API call fails.
        """
        paths = self._prepare_refresh(tags)
        response, http_response = await self._api.as_async.get(
            "/tags", params={"path": paths, "take": str(len(tags))}
        )
        self._handle_refresh(tags, response, http_response)

    def _prepare_refresh(self, tags: List[tbase.TagData]) -> str:
        if tags is None:
            raise ValueError("tags cannot be None")
        elif any(t is None for t in tags):
            raise ValueError("Tags cannot contain None")

        return ",".join(t.validate_path() for t in tags)

    def _handle_refresh(
        self,
        tags: List[tbase.TagData],
        refresh_result: Dict[str, Any],
        http_response: HttpResponse,
    ) -> None:
        if refresh_result is None or refresh_result.get("tags") is None:
            raise self.invalid_response(http_response)

        read_tags = {t["path"]: t for t in refresh_result["tags"]}

        for data in tags:
            tag = read_tags.get(data.path)
            if tag is not None:
                data.clear_retention()
                data.data_type = tbase.DataType.from_api_name(
                    tag.get("type") or "UNKNOWN"
                )
                data.replace_keywords(tag.get("keywords") or [])
                data.replace_properties(tag.get("properties") or {})
                data.collect_aggregates = tag.get("collectAggregates") or False
            else:
                data.data_type = tbase.DataType.UNKNOWN

    def query(
        self,
        paths: Optional[Sequence[str]] = None,
        keywords: Optional[Iterable[str]] = None,
        properties: Optional[Dict[str, str]] = None,
        *,
        skip: int = 0,
        take: Optional[int] = None
    ) -> tbase.TagQueryResultCollection:
        """Query the server for available tags matching the given criteria.

        Args:
            paths: List of tag paths to include in the result. May include glob-style
                wildcards.
            keywords: List of keywords that tags must have, or None.
            properties: Mapping of properties and their values that tags must have, or
                None.
            skip: The number of tags to initially skip in the results.
            take: The number of tags to include in each page of results.

        Returns:
            A :class:`TagQueryResultCollection` containing the first page of results.
            Enumerating the collection will retrieve additional pages according to the
            ``take`` parameter.

        Raises:
            ValueError: if ``skip`` or ``take`` is negative.
            ValueError: if ``paths`` is an empty list.
            ValueError: if any of ``paths`` are None.
            ApiException: if the API call fails.
        """
        path_str, keyword_str, prop_str = self._prepare_query(
            paths, keywords, properties, skip, take
        )
        params = {
            "path": path_str,
            "keywords": keyword_str,
            "properties": prop_str,
            "skip": str(skip) if skip is not None else None,
            "take": str(take) if take is not None else None,
        }
        for k, v in list(params.items()):
            if v is None:
                del params[k]
        first_page, http_response = self._api.get("/tags", params=params)
        return HttpTagQueryResultCollection(
            self._http_client,
            path_str,
            keyword_str,
            prop_str,
            skip,
            take,
            first_page,
            http_response,
        )

    async def query_async(
        self,
        paths: Optional[Sequence[str]] = None,
        keywords: Optional[Iterable[str]] = None,
        properties: Optional[Dict[str, str]] = None,
        *,
        skip: int = 0,
        take: Optional[int] = None
    ) -> tbase.AsyncTagQueryResultCollection:
        """Asynchronously query the server for available tags matching the given criteria.

        Args:
            paths: List of tag paths to include in the result. May include glob-style
                wildcards.
            keywords: List of keywords that tags must have, or None.
            properties: Mapping of properties and their values that tags must have, or
                None.
            skip: The number of tags to initially skip in the results.
            take: The number of tags to include in each page of results.

        Returns:
            A task representing the asynchronous operation. On success, contains a
            :class:`TagQueryResultCollection` containing the first page of results.
            Enumerating the collection will retrieve additional pages according to the
            ``take`` parameter.

        Raises:
            ValueError: if ``skip`` is negative.
            ValueError: if ``take`` is negative.
            ApiException: if the API call fails.
        """
        path_str, keyword_str, prop_str = self._prepare_query(
            paths, keywords, properties, skip, take
        )
        params = {
            "path": path_str,
            "keywords": keyword_str,
            "properties": prop_str,
            "skip": str(skip) if skip is not None else None,
            "take": str(take) if take is not None else None,
        }
        for k, v in list(params.items()):
            if v is None:
                del params[k]
        first_page, http_response = await self._api.as_async.get("/tags", params=params)
        return HttpAsyncTagQueryResultCollection(
            self._http_client,
            path_str,
            keyword_str,
            prop_str,
            skip,
            take,
            first_page,
            http_response,
        )

    def _prepare_query(
        self,
        paths: Optional[Sequence[str]],
        keywords: Optional[Iterable[str]],
        properties: Optional[Dict[str, str]],
        skip: Optional[int],
        take: Optional[int] = None,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        if paths is not None and len(paths) == 0:
            raise ValueError("paths cannot be empty an empty list")
        if paths is not None and any(p is None for p in paths):
            raise ValueError("paths cannot contain None")
        if skip is not None and skip < 0:
            raise ValueError("skip cannot be negative")
        if take is not None and take < 0:
            raise ValueError("take cannot be negative")

        path_str = None
        keyword_str = None
        prop_str = None

        if paths is not None:
            path_str = ",".join(tbase.TagPathUtilities.validate_query(p) for p in paths)
        if keywords:
            keyword_str = ",".join(keywords)
        if properties:
            prop_str = ",".join("{}={}".format(k, v) for k, v in properties.items())

        return path_str, keyword_str, prop_str

    def update(
        self, updates: Union[Sequence[tbase.TagData], Sequence[tbase.TagDataUpdate]]
    ) -> None:
        """Update the metadata of one or more tags on the server, creating tags that don't exist.

        If ``updates`` contains :class:`TagData` objects, existing metadata will be
        replaced. If ``updates`` contains :class:`TagDataUpdate` objects instead, tags
        that already exist will have their existing keywords, properties, and settings
        merged with those specified in the corresponding :class:`TagDataUpdate`.

        The call fails if any of the tags already exist as a different data type.

        Args:
            updates: The tags to update (if :class:`TagData` objects are given), or the
                tag metadata updates to send (if :class:`TagDataUpdate` objects are
                given).

        Raises:
            ValueError: if ``updates`` is None or empty.
            ValueError: if ``updates`` contains any invalid tags.
            ValueError: if ``updates`` contains both ``TagData`` objects and
                ``TagDataUpdate`` objects.
            ApiException: if the API call fails.
        """
        tag_models, merge = self._prepare_update(updates)
        partial_success, _ = self._api.post(
            "/update-tags", data={"tags": tag_models, "merge": merge}
        )

        if partial_success is not None:
            err_dict = partial_success.get("error")
            if err_dict is None and "code" in partial_success:
                # SystemLink Cloud has a bug in which it returns the error directly
                # instead of under the "error" key
                err_dict = partial_success
            err_obj = core.ApiError.parse_obj(err_dict) if err_dict else None
            if err_dict is None:
                assert False, partial_success
            raise core.ApiException(error=err_obj)

    async def update_async(
        self, updates: Union[Sequence[tbase.TagData], Sequence[tbase.TagDataUpdate]]
    ) -> None:
        """Asynchronously update the metadata of one or more tags on the server, creating tags that don't exist.

        If ``updates`` contains :class:`TagData` objects, existing metadata will be
        replaced. If ``updates`` contains :class:`TagDataUpdate` objects instead, tags
        that already exist will have their existing keywords, properties, and settings
        merged with those specified in the corresponding :class:`TagDataUpdate`.

        Args:
            updates: The tags to update (if :class:`TagData` objects are given), or the
                tag metadata updates to send (if :class:`TagDataUpdate` objects are
                given).

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ValueError: if ``updates`` is None or empty.
            ValueError: if ``updates`` contains any invalid tags.
            ValueError: if ``updates`` contains both ``TagData`` objects and
                ``TagDataUpdate`` objects.
            ApiException: if the API call fails.
        """
        tag_models, merge = self._prepare_update(updates)
        partial_success, _ = await self._api.as_async.post(
            "/update-tags", data={"tags": tag_models, "merge": merge}
        )

        if partial_success is not None:
            err_dict = partial_success.get("error")
            if err_dict is None and "code" in partial_success:
                # SystemLink Cloud has a bug in which it returns the error directly
                # instead of under the "error" key
                err_dict = partial_success
            err_obj = core.ApiError.parse_obj(err_dict) if err_dict else None
            if err_dict is None:
                assert False, partial_success
            raise core.ApiException(error=err_obj)

    def _prepare_update(
        self, updates: Union[Sequence[tbase.TagData], Sequence[tbase.TagDataUpdate]]
    ) -> Tuple[List[Dict[str, Any]], bool]:
        if updates is None:
            raise ValueError("updates cannot be None")
        if not updates:
            raise ValueError("updates cannot be empty")
        if not all(isinstance(u, type(updates[0])) for u in updates):
            raise ValueError(
                "updates must contain only TagData objects or TagDataUpdate objects, not both"
            )

        merge = isinstance(updates[0], tbase.TagDataUpdate)

        return [u.to_json_dict() for u in updates], merge

    def delete(self, tags: Iterable[Union[tbase.TagData, str]]) -> None:
        """Delete one or more tags from the server.

        Args:
            tags: The tags (or tag paths) to delete.

        Raises:
            ValueError: if ``tags`` is None.
            ValueError: if ``tags`` contains any invalid tags.
            ApiException: if the API call fails.
        """
        if tags is None:
            raise ValueError("tags cannot be None")
        if any(t is None for t in tags):
            raise ValueError("tags cannot contain None")

        validated_paths = [
            tbase.TagPathUtilities.validate(t)
            if isinstance(t, str)
            else t.validate_path()
            for t in tags
        ]

        self._perform_delete(validated_paths)

    def delete_async(
        self, tags: Iterable[Union[tbase.TagData, str]] = None
    ) -> Awaitable[None]:
        """Asynchronously delete one or more tags from the server.

        Args:
            tags: The tags (or tag paths) to delete.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ValueError: if ``tags`` is None.
            ValueError: if ``tags`` contains any invalid tags.
            ApiException: if the API call fails.
        """
        try:
            if tags is None:
                raise ValueError("tags cannot be None")
            if any(t is None for t in tags):
                raise ValueError("tags cannot contain None")

            validated_paths = [
                tbase.TagPathUtilities.validate(t)
                if isinstance(t, str)
                else t.validate_path()
                for t in tags
            ]
        except Exception as ex:
            f = asyncio.get_event_loop().create_future()
            f.set_exception(ex)
            return f

        return self._perform_delete_async(validated_paths)

    def _perform_delete(self, paths: List[str]) -> None:
        if len(paths) < 4:
            # Few enough to make multiple, single deletes rather than creating a selection.
            exceptions = []

            for path in paths:
                try:
                    self._api.delete(
                        "/tags/{path}",
                        params={"path": tbase.TagPathUtilities.validate(path)},
                    )
                except core.ApiException as ex:
                    exceptions.append(ex)

            if exceptions:
                raise exceptions[0] from None
        else:
            with TemporaryTagSelection.create(self._http_client, paths) as selection:
                self._api.delete("/selections/{id}/tags", params={"id": selection.id})

    async def _perform_delete_async(self, paths: List[str]) -> None:
        if len(paths) < 4:
            # Few enough to make multiple, single deletes rather than creating a selection.
            await asyncio.gather(
                *[
                    self._api.as_async.delete(
                        "/tags/{path}",
                        params={"path": tbase.TagPathUtilities.validate(p)},
                    )
                    for p in paths
                ]
            )
        else:
            async with await TemporaryTagSelection.create_async(
                self._http_client, paths
            ) as selection:
                await self._api.as_async.delete(
                    "/selections/{id}/tags", params={"id": selection.id}
                )

    def create_writer(
        self,
        *,
        buffer_size: Optional[int] = None,
        max_buffer_time: Optional[datetime.timedelta] = None
    ) -> tbase.BufferedTagWriter:
        """Create a tag writer that buffers tag values until
        :meth:`~BufferedTagWriter.send_buffered_writes()` is called on the returned
        object, ``buffer_size`` writes have been buffered, or ``max_buffer_time`` time
        has past since buffering a value, at which point the writes will be sent
        automatically.

        Args:
            buffer_size: The maximum number of tag writes to buffer before automatically
                sending them to the server.
            max_buffer_time: The amount of time before writes are sent.

        Returns:
            The created writer. Close the writer to free resources.

        Raises:
            ValueError: if ``buffer_size`` and ``max_buffer_time`` are both None.
            ValueError: if ``buffer_size`` is less than one.
        """
        if buffer_size is None and max_buffer_time is None:
            raise ValueError("must provide either buffer_size or max_buffer_time")

        if buffer_size is not None:
            if buffer_size < 1:
                raise ValueError("buffer_size cannot be 0 or negative")
        else:
            buffer_size = 0

        if max_buffer_time is not None:
            if max_buffer_time.total_seconds() < 0.001:
                raise ValueError("max_buffer_time must be at least 1 millisecond")
            timer = ManualResetTimer(max_buffer_time)
        else:
            timer = ManualResetTimer.null_timer

        return HttpBufferedTagWriter(
            self._http_client, SystemTimeStamper(), buffer_size, timer
        )

    def _read(
        self, path: str, include_timestamp: bool, include_aggregates: bool
    ) -> Optional[SerializedTagWithAggregates]:
        """Retrieve the current value of the tag with the given ``path`` from the server.

        Optionally retrieves the aggregate values as well. The tag must exist. Clients
        do not typically call this method directly. Use a :class:`.TagValueReader`
        instead.

        Args:
            path: The path of the tag to read.
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value serialized as a string, along with timestamp and/or aggregates, if
            requested, or None if the tag exists but doesn't have a value.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` is None.
            ApiException: if the API call fails.
        """
        path = tbase.TagPathUtilities.validate(path)

        if include_aggregates:
            response, http_response = self._api.get(
                "/tags/{path}/values", params={"path": path}
            )
            return self._handle_read(
                path, response, http_response, include_timestamp, True
            )
        elif include_timestamp:
            response2, http_response = self._api.get(
                "/tags/{path}/values/current", params={"path": path}
            )
            return self._handle_read(
                path, response2, http_response, include_timestamp, False
            )
        else:
            response3, http_response = self._api.get(
                "/tags/{path}/values/current/value", params={"path": path}
            )
            return self._handle_read(path, response3, http_response)

    async def _read_async(
        self, path: str, include_timestamp: bool, include_aggregates: bool
    ) -> Optional[SerializedTagWithAggregates]:
        """Asynchronously retrieve the current value of the tag with the given ``path`` from the server.

        Optionally retrieves the aggregate values as well. The tag must exist. Clients
        do not typically call this method directly. Use a :class:`.TagValueReader`
        instead.

        Args:
            path: The path of the tag to read.
            include_timestamp: True to include the timestamp associated with the value
                in the result.
            include_aggregates: True to include the tag's aggregate values in the result
                if the tag is set to :attr:`TagData.collect_aggregates`.

        Returns:
            The value serialized as a string, or None if the tag exists but doesn't have
            a value.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` is None.
            ApiException: if the API call fails.
        """
        path = tbase.TagPathUtilities.validate(path)

        if include_aggregates:
            response, http_response = await self._api.as_async.get(
                "/tags/{path}/values", params={"path": path}
            )
            return self._handle_read(
                path, response, http_response, include_timestamp, True
            )
        elif include_timestamp:
            response2, http_response = await self._api.as_async.get(
                "/tags/{path}/values/current", params={"path": path}
            )
            return self._handle_read(
                path, response2, http_response, include_timestamp, False
            )
        else:
            response3, http_response = await self._api.as_async.get(
                "/tags/{path}/values/current/value", params={"path": path}
            )
            return self._handle_read(path, response3, http_response)

    def _handle_read(
        self,
        path: str,
        response: Dict[str, Any],
        http_response: HttpResponse,
        include_timestamp: Optional[bool] = False,
        include_aggregates: Optional[bool] = False,
    ) -> Optional[SerializedTagWithAggregates]:
        if response is None:
            return None

        agg = response.get("aggregates") or {}  # type: Dict[str, Any]
        current = response.get("current", response)  # type: Dict[str, Any]
        if current is None:
            return None

        if "type" in response:
            val = response
        else:
            val = current["value"]
        if val is None:
            return None

        assert "value" in val

        timestamp = None  # type: Optional[datetime.datetime]
        if include_timestamp:
            if current.get("timestamp") is None:
                raise self.invalid_response(http_response)

            timestamp = TimestampUtilities.str_to_datetime(current["timestamp"])

        return SerializedTagWithAggregates(
            path,
            tbase.DataType.from_api_name(val["type"]),
            val["value"],
            timestamp,
            agg.get("count"),
            agg.get("min"),
            agg.get("max"),
            float(agg["avg"]) if agg.get("avg") is not None else None,
        )

    @classmethod
    def invalid_response(cls, response: HttpResponse) -> core.ApiException:
        request = response.request
        return core.ApiException(
            "Invalid response from {} {}".format(request.method, request.url)
        )
