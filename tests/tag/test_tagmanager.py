import asyncio
import time
import uuid
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from unittest import mock

import pytest  # type: ignore
from systemlink.clients import core, tag as tbase

from .http.httpclienttestbase import HttpClientTestBase, MockResponse
from ..anyorderlist import AnyOrderList


class TestTagManager(HttpClientTestBase):
    def setup_method(self, method):
        super().setup_method(method)

        def get_client_mock(*args, **kwargs):
            return self._client

        with mock.patch(
            "systemlink.clients.tag._tag_manager.HttpClient", get_client_mock
        ):
            self._uut = tbase.TagManager(object())

    def test__metadata_supplied__create_selection__metadata_used_without_query(self):
        tags = [
            tbase.TagData("tag1"),
            tbase.TagData("tag2", tbase.DataType.BOOLEAN),
            tbase.TagData(
                "tag3", tbase.DataType.DATE_TIME, ["keyword1"], {"prop1": "value1"}
            ),
        ]

        selection = self._uut.create_selection(tags)

        assert self._client.all_requests.call_count == 0
        assert [t.path for t in tags] == sorted(selection.paths)
        assert tags == list(sorted(selection.metadata.values(), key=(lambda t: t.path)))
        assert [t.path for t in tags[1:]] == sorted(selection.values.keys())
        assert selection.values[tags[1].path].data_type == tbase.DataType.BOOLEAN
        assert selection.values[tags[2].path].data_type == tbase.DataType.DATE_TIME

    def test__open_selection__creates_selection_and_queries_tags(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        token = uuid.uuid4()

        def mock_request(method, uri, params=None, data=None):
            if (method, uri) == ("POST", "/nitag/v2/selections"):
                ret = dict(data) if data else {}
                ret["id"] = token
                return ret, MockResponse(method, uri)
            elif (method, uri) == ("GET", "/nitag/v2/selections/{id}/tags"):
                return (
                    [
                        {"type": "BOOLEAN", "path": path1},
                        {"type": "DOUBLE", "path": path2},
                    ],
                    MockResponse(method, uri),
                )
            elif (method, uri) == ("DELETE", "/nitag/v2/selections/{id}"):
                return None, MockResponse(method, uri)
            else:
                assert False, (method, uri)

        self._client.all_requests.configure_mock(side_effect=mock_request)

        selection = self._uut.open_selection(paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]
        assert 2 == len(selection.metadata)

    @pytest.mark.asyncio
    async def test__open_selection_async__creates_selection_and_queries_tags(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        token = uuid.uuid4()

        def mock_request(method, uri, params=None, data=None):
            if (method, uri) == ("POST", "/nitag/v2/selections"):
                ret = dict(data) if data else {}
                ret["id"] = token
                return ret, MockResponse(method, uri)
            elif (method, uri) == ("GET", "/nitag/v2/selections/{id}/tags"):
                return (
                    [
                        {"type": "BOOLEAN", "path": path1},
                        {"type": "DOUBLE", "path": path2},
                    ],
                    MockResponse(method, uri),
                )
            elif (method, uri) == ("DELETE", "/nitag/v2/selections/{id}"):
                return None, MockResponse(method, uri)
            else:
                assert False, (method, uri)

        self._client.all_requests.configure_mock(side_effect=mock_request)

        selection = await self._uut.open_selection_async(paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]
        assert 2 == len(selection.metadata)

    def test__bag_arguments__open__raises(self):
        with pytest.raises(ValueError):
            self._uut.open(None)
        with pytest.raises(ValueError):
            self._uut.open(None, tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            self._uut.open(None, tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            self._uut.open("")
        with pytest.raises(ValueError):
            self._uut.open("", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            self._uut.open("", tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            self._uut.open(" ")
        with pytest.raises(ValueError):
            self._uut.open(" ", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            self._uut.open(" ", tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            self._uut.open("*")
        with pytest.raises(ValueError):
            self._uut.open("*", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            self._uut.open("*", tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            self._uut.open("tag", tbase.DataType.UNKNOWN)
        with pytest.raises(ValueError):
            self._uut.open("tag", tbase.DataType.UNKNOWN, create=True)

    def test__existing_tag__open_without_datatype__retrieves_tag(self):
        path = "tag1"
        public_properties = {"prop1": "value1", "prop2": "value2"}
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "type": "BOOLEAN",
                        "properties": all_properties,
                        "path": path,
                        "keywords": keywords,
                        "collectAggregates": True,
                    }
                ]
            )
        )

        tag = self._uut.open(path)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": path}
        )
        assert tag is not None
        assert tbase.DataType.BOOLEAN == tag.data_type
        assert tag.collect_aggregates is True
        assert keywords == sorted(tag.keywords)
        assert sorted(public_properties.items()) == sorted(tag.properties.items())
        assert dummy_tag.retention_count == tag.retention_count
        assert dummy_tag.retention_days == tag.retention_days
        assert dummy_tag.retention_type == tag.retention_type

    def test___tag_not_found__open_without_datatype__raises(self):
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        ex = core.ApiException("404 tag not found", err)
        self._client.all_requests.configure_mock(side_effect=ex)

        with pytest.raises(core.ApiException) as actual:
            self._uut.open("tag")
        assert ex is actual.value

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": "tag"}
        )

    def test___tag_not_found__open_with_datatype__creates_tag(self):
        path = "tag"
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [core.ApiException("404 tag not found", err), None]
            )
        )

        tag = self._uut.open(path, tbase.DataType.UINT64)

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call(
                "POST",
                "/nitag/v2/tags",
                params=None,
                data={"path": path, "type": "U_INT64"},
            ),
        ]
        assert path == tag.path
        assert tbase.DataType.UINT64 == tag.data_type
        assert not tag.collect_aggregates
        assert 0 == len(tag.keywords)
        assert 0 == len(tag.properties)
        assert tag.retention_count is None
        assert tag.retention_days is None
        assert tbase.RetentionType.NONE == tag.retention_type

    def test___tag_not_found__open_with_create_true__creates_tag(self):
        path = "tag"
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [core.ApiException("404 tag not found", err), None]
            )
        )

        tag = self._uut.open(path, tbase.DataType.UINT64, create=True)

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call(
                "POST",
                "/nitag/v2/tags",
                params=None,
                data={"path": path, "type": "U_INT64"},
            ),
        ]
        assert path == tag.path
        assert tbase.DataType.UINT64 == tag.data_type
        assert not tag.collect_aggregates
        assert 0 == len(tag.keywords)
        assert 0 == len(tag.properties)
        assert tag.retention_count is None
        assert tag.retention_days is None
        assert tbase.RetentionType.NONE == tag.retention_type

    def test__tag_exists__open__does_not_create_tag(self):
        path = "tag1"
        public_properties = {"prop1": "value1", "prop2": "value2"}
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "type": "BOOLEAN",
                        "properties": all_properties,
                        "path": path,
                        "keywords": keywords,
                        "collectAggregates": True,
                    }
                ]
            )
        )

        tag = self._uut.open(path, tbase.DataType.BOOLEAN, create=True)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": "tag1"}
        )
        assert tag is not None
        assert tbase.DataType.BOOLEAN == tag.data_type
        assert tag.collect_aggregates is True
        assert keywords == sorted(tag.keywords)
        assert sorted(public_properties.items()) == sorted(tag.properties.items())
        assert dummy_tag.retention_count == tag.retention_count
        assert dummy_tag.retention_days == tag.retention_days
        assert dummy_tag.retention_type == tag.retention_type

    def test__tag_not_found__open_with_create_False__raises(self):
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        ex = core.ApiException("404 tag not found", err)
        self._client.all_requests.configure_mock(side_effect=ex)

        with pytest.raises(core.ApiException) as actual:
            self._uut.open("tag", tbase.DataType.DOUBLE, create=False)
        assert ex is actual.value

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": "tag"}
        )

    def test__tag_exists_with_different_datatype__open__raises(self):
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([{"type": "BOOLEAN", "path": "tag"}] * 3)
        )
        with pytest.raises(core.ApiException):
            self._uut.open("tag", tbase.DataType.DOUBLE)
        with pytest.raises(core.ApiException):
            self._uut.open("tag", tbase.DataType.DOUBLE, create=False)
        with pytest.raises(core.ApiException):
            self._uut.open("tag", tbase.DataType.DOUBLE, create=True)

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
        ]

    @pytest.mark.asyncio
    async def test__bag_arguments__open_async__raises(self):
        with pytest.raises(ValueError):
            await self._uut.open_async(None)
        with pytest.raises(ValueError):
            await self._uut.open_async(None, tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            await self._uut.open_async(None, tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            await self._uut.open_async("")
        with pytest.raises(ValueError):
            await self._uut.open_async("", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            await self._uut.open_async("", tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            await self._uut.open_async(" ")
        with pytest.raises(ValueError):
            await self._uut.open_async(" ", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            await self._uut.open_async(" ", tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            await self._uut.open_async("*")
        with pytest.raises(ValueError):
            await self._uut.open_async("*", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            await self._uut.open_async("*", tbase.DataType.BOOLEAN, create=True)
        with pytest.raises(ValueError):
            await self._uut.open_async("tag", tbase.DataType.UNKNOWN)
        with pytest.raises(ValueError):
            await self._uut.open_async("tag", tbase.DataType.UNKNOWN, create=True)

    @pytest.mark.asyncio
    async def test__existing_tag__open_async_without_datatype__retrieves_tag(self):
        path = "tag1"
        public_properties = {"prop1": "value1", "prop2": "value2"}
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "type": "BOOLEAN",
                        "properties": all_properties,
                        "path": path,
                        "keywords": keywords,
                        "collectAggregates": True,
                    }
                ]
            )
        )

        tag = await self._uut.open_async(path)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": "tag1"}
        )
        assert tag is not None
        assert tbase.DataType.BOOLEAN == tag.data_type
        assert tag.collect_aggregates is True
        assert keywords == sorted(tag.keywords)
        assert sorted(public_properties.items()) == sorted(tag.properties.items())
        assert dummy_tag.retention_count == tag.retention_count
        assert dummy_tag.retention_days == tag.retention_days
        assert dummy_tag.retention_type == tag.retention_type

    @pytest.mark.asyncio
    async def test___tag_not_found__open_async_without_datatype__raises(self):
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        ex = core.ApiException("404 tag not found", err)
        self._client.all_requests.configure_mock(side_effect=ex)

        with pytest.raises(core.ApiException) as actual:
            await self._uut.open_async("tag")
        assert ex is actual.value

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": "tag"}
        )

    @pytest.mark.asyncio
    async def test___tag_not_found__open_async_with_datatype__creates_tag(self):
        path = "tag"
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [core.ApiException("404 tag not found", err), None]
            )
        )

        tag = await self._uut.open_async(path, tbase.DataType.UINT64)

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call(
                "POST",
                "/nitag/v2/tags",
                params=None,
                data={"path": path, "type": "U_INT64"},
            ),
        ]
        assert path == tag.path
        assert tbase.DataType.UINT64 == tag.data_type
        assert not tag.collect_aggregates
        assert 0 == len(tag.keywords)
        assert 0 == len(tag.properties)
        assert tag.retention_count is None
        assert tag.retention_days is None
        assert tbase.RetentionType.NONE == tag.retention_type

    @pytest.mark.asyncio
    async def test___tag_not_found__open_async_with_create_true__creates_tag(self):
        path = "tag"
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [core.ApiException("404 tag not found", err), None]
            )
        )

        tag = await self._uut.open_async(path, tbase.DataType.UINT64, create=True)

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call(
                "POST",
                "/nitag/v2/tags",
                params=None,
                data={"path": path, "type": "U_INT64"},
            ),
        ]
        assert path == tag.path
        assert tbase.DataType.UINT64 == tag.data_type
        assert not tag.collect_aggregates
        assert 0 == len(tag.keywords)
        assert 0 == len(tag.properties)
        assert tag.retention_count is None
        assert tag.retention_days is None
        assert tbase.RetentionType.NONE == tag.retention_type

    @pytest.mark.asyncio
    async def test__tag_exists__open_async__does_not_create_tag(self):
        path = "tag1"
        public_properties = {"prop1": "value1", "prop2": "value2"}
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "type": "BOOLEAN",
                        "properties": all_properties,
                        "path": path,
                        "keywords": keywords,
                        "collectAggregates": True,
                    }
                ]
            )
        )

        tag = await self._uut.open_async(path, tbase.DataType.BOOLEAN, create=True)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": "tag1"}
        )
        assert tag is not None
        assert tbase.DataType.BOOLEAN == tag.data_type
        assert tag.collect_aggregates is True
        assert keywords == sorted(tag.keywords)
        assert sorted(public_properties.items()) == sorted(tag.properties.items())
        assert dummy_tag.retention_count == tag.retention_count
        assert dummy_tag.retention_days == tag.retention_days
        assert dummy_tag.retention_type == tag.retention_type

    @pytest.mark.asyncio
    async def test__tag_not_found__open_async_with_create_False__raises(self,):
        err = core.ApiError()
        err.name = "Tag.NoSuchTag"
        ex = core.ApiException("404 tag not found", err)
        self._client.all_requests.configure_mock(side_effect=ex)

        with pytest.raises(core.ApiException) as actual:
            await self._uut.open_async("tag", tbase.DataType.DOUBLE, create=False)
        assert ex is actual.value

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}", params={"path": "tag"}
        )

    @pytest.mark.asyncio
    async def test__tag_exists_with_different_datatype__open_async__raises(self,):
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([{"type": "BOOLEAN", "path": "tag"}] * 3)
        )
        with pytest.raises(core.ApiException):
            await self._uut.open_async("tag", tbase.DataType.DOUBLE)
        with pytest.raises(core.ApiException):
            await self._uut.open_async("tag", tbase.DataType.DOUBLE, create=False)
        with pytest.raises(core.ApiException):
            await self._uut.open_async("tag", tbase.DataType.DOUBLE, create=True)

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
            mock.call("GET", "/nitag/v2/tags/{path}", params={"path": "tag"}),
        ]

    def test__invalid_tags__refresh__raises(self):
        with pytest.raises(ValueError):
            self._uut.refresh(None)
        with pytest.raises(ValueError):
            self._uut.refresh([None])
        with pytest.raises(ValueError):
            self._uut.refresh([tbase.TagData("tag"), None])
        with pytest.raises(ValueError):
            self._uut.refresh([tbase.TagData("tag"), tbase.TagData(None)])
        with pytest.raises(ValueError):
            self._uut.refresh([tbase.TagData("tag"), tbase.TagData("")])

    def test__multiple_tags_given__refresh__all_tags_updated(self):
        path1 = "tag1"
        path2 = "tag2"
        public_properties = {"prop1": "value1", "prop2": "value2"}
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path1)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": 2,
                        "tags": [
                            {
                                "type": "BOOLEAN",
                                "properties": all_properties,
                                "path": path1,
                                "keywords": keywords,
                                "collectAggregates": True,
                            },
                            {"type": "DOUBLE", "path": path2},
                        ],
                    }
                ]
            )
        )
        tag1 = tbase.TagData(path1)
        tag2 = tbase.TagData(
            path2, tbase.DataType.UINT64, ["dummy"], {"dummy": "dummy"}
        )
        tag2.set_retention_count(9)

        self._uut.refresh([tag1, tag2])

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": path1 + "," + path2, "take": "2"}
        )
        assert tbase.DataType.BOOLEAN == tag1.data_type
        assert tag1.collect_aggregates is True
        assert keywords == sorted(tag1.keywords)
        assert sorted(public_properties.items()) == sorted(tag1.properties.items())
        assert dummy_tag.retention_count == tag1.retention_count
        assert dummy_tag.retention_days == tag1.retention_days
        assert dummy_tag.retention_type == tag1.retention_type

        assert tbase.DataType.DOUBLE == tag2.data_type
        assert tag2.collect_aggregates is False
        assert 0 == len(tag2.keywords)
        assert 0 == len(tag2.properties)
        assert tag2.retention_count is None
        assert tag2.retention_days is None
        assert tbase.RetentionType.NONE == tag2.retention_type

    def test__missing_tags_supplied__refresh__missing_tags_ignored(self):
        keywords = ["keyword"]
        properties = {"prop": "value"}
        tag1 = tbase.TagData("existing")
        tag2 = tbase.TagData("missing", tbase.DataType.DOUBLE, keywords, properties)
        tag2.collect_aggregates = True
        tag2.set_retention_days(6)
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"totalCount": 1, "tags": [{"type": "BOOLEAN", "path": "existing"}]}]
            )
        )

        self._uut.refresh([tag1, tag2])

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": "existing,missing", "take": "2"}
        )
        assert tbase.DataType.BOOLEAN == tag1.data_type
        assert tbase.DataType.UNKNOWN == tag2.data_type
        assert tag2.collect_aggregates is True
        assert keywords == tag2.keywords
        assert properties == tag2.properties
        assert tag2.retention_count is None
        assert 6 == tag2.retention_days
        assert tbase.RetentionType.DURATION == tag2.retention_type

    @pytest.mark.asyncio
    async def test__invalid_tags__refresh_async__raises(self):
        with pytest.raises(ValueError):
            await self._uut.refresh_async(None)
        with pytest.raises(ValueError):
            await self._uut.refresh_async([None])
        with pytest.raises(ValueError):
            await self._uut.refresh_async([tbase.TagData("tag"), None])
        with pytest.raises(ValueError):
            await self._uut.refresh_async([tbase.TagData("tag"), tbase.TagData(None)])
        with pytest.raises(ValueError):
            await self._uut.refresh_async([tbase.TagData("tag"), tbase.TagData("")])

    @pytest.mark.asyncio
    async def test__multiple_tags_given__refresh_async__all_tags_updated(self):
        path1 = "tag1"
        path2 = "tag2"
        public_properties = {"prop1": "value1", "prop2": "value2"}
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path1)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": 2,
                        "tags": [
                            {
                                "type": "BOOLEAN",
                                "properties": all_properties,
                                "path": path1,
                                "keywords": keywords,
                                "collectAggregates": True,
                            },
                            {"type": "DOUBLE", "path": path2},
                        ],
                    }
                ]
            )
        )

        tag1 = tbase.TagData(path1)
        tag2 = tbase.TagData(
            path2, tbase.DataType.UINT64, ["dummy"], {"dummy": "dummy"}
        )
        tag2.set_retention_count(9)
        await self._uut.refresh_async([tag1, tag2])

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": path1 + "," + path2, "take": "2"}
        )
        assert tbase.DataType.BOOLEAN == tag1.data_type
        assert tag1.collect_aggregates is True
        assert keywords == sorted(tag1.keywords)
        assert sorted(public_properties.items()) == sorted(tag1.properties.items())
        assert dummy_tag.retention_count == tag1.retention_count
        assert dummy_tag.retention_days == tag1.retention_days
        assert dummy_tag.retention_type == tag1.retention_type

        assert tbase.DataType.DOUBLE == tag2.data_type
        assert tag2.collect_aggregates is False
        assert 0 == len(tag2.keywords)
        assert 0 == len(tag2.properties)
        assert tag2.retention_count is None
        assert tag2.retention_days is None
        assert tbase.RetentionType.NONE == tag2.retention_type

    @pytest.mark.asyncio
    async def test__missing_tags_supplied__refresh_async__missing_tags_ignored(self):
        keywords = ["keyword"]
        properties = {"prop": "value"}
        tag1 = tbase.TagData("existing")
        tag2 = tbase.TagData("missing", tbase.DataType.DOUBLE, keywords, properties)
        tag2.collect_aggregates = True
        tag2.set_retention_days(6)
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"totalCount": 1, "tags": [{"type": "BOOLEAN", "path": "existing"}]}]
            )
        )

        await self._uut.refresh_async([tag1, tag2])

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": "existing,missing", "take": "2"}
        )
        assert tbase.DataType.BOOLEAN == tag1.data_type
        assert tbase.DataType.UNKNOWN == tag2.data_type
        assert tag2.collect_aggregates is True
        assert keywords == tag2.keywords
        assert properties == tag2.properties
        assert tag2.retention_count is None
        assert 6 == tag2.retention_days
        assert tbase.RetentionType.DURATION == tag2.retention_type

    def test__bad_arguments__query__raises(self):
        with pytest.raises(ValueError):
            self._uut.query(skip=-1, take=0)
        with pytest.raises(ValueError):
            self._uut.query(skip=0, take=-1)

        with pytest.raises(ValueError):
            self._uut.query([])
        with pytest.raises(ValueError):
            self._uut.query(["tag", None])
        with pytest.raises(ValueError):
            self._uut.query(["tag", ""])
        with pytest.raises(ValueError):
            self._uut.query(["tag", " "])

        with pytest.raises(ValueError):
            self._uut.query([], skip=0, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag", None], skip=0, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag", ""], skip=0, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag", " "], skip=0, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag"], skip=-1, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag"], skip=0, take=-1)

        with pytest.raises(ValueError):
            self._uut.query(["tag", None], None, None)
        with pytest.raises(ValueError):
            self._uut.query(["tag", ""], None, None)
        with pytest.raises(ValueError):
            self._uut.query(["tag", " "], None, None)

        with pytest.raises(ValueError):
            self._uut.query(["tag", None], None, None, skip=0, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag", ""], None, None, skip=0, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag", " "], None, None, skip=0, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag"], None, None, skip=-1, take=0)
        with pytest.raises(ValueError):
            self._uut.query(["tag"], None, None, skip=0, take=-1)

    def test__only_skip_and_take_supplied__query__performs_query(self):
        total_count = 4
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "BOOLEAN", "path": path1}],
                    },
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "DATE_TIME", "path": path2}],
                    },
                ]
            )
        )

        result = self._uut.query(skip=2, take=1)

        assert total_count == result.total_count
        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"skip": "2", "take": "1"}
        )
        pages = list(result)

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags", params={"skip": "2", "take": "1"}),
            mock.call("GET", "/nitag/v2/tags", params={"skip": "3", "take": "1"}),
        ]

        assert 2 == len(pages)
        assert 1 == len(pages[0])
        assert path1 == pages[0][0].path
        assert tbase.DataType.BOOLEAN == pages[0][0].data_type
        assert 1 == len(pages[1])
        assert path2 == pages[1][0].path
        assert tbase.DataType.DATE_TIME == pages[1][0].data_type

    def test__only_paths_supplied__query__performs_query(self):
        total_count = 0
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([{"totalCount": 0, "tags": []}])
        )

        result = self._uut.query(["tag1", "tag2"])

        assert total_count == result.total_count
        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": "tag1,tag2", "skip": "0"}
        )

    def test__path_with_skip_and_take_supplied__query__performs_query(self):
        total_count = 4
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "BOOLEAN", "path": path1}],
                    },
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "DATE_TIME", "path": path2}],
                    },
                ]
            )
        )

        result = self._uut.query(
            ["missing1", path1, "missing2", path2, "missing3"], skip=2, take=1
        )
        assert total_count == result.total_count
        paths = ",".join(("missing1", path1, "missing2", path2, "missing3"))
        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": paths, "skip": "2", "take": "1"}
        )

        pages = list(result)
        assert self._client.all_requests.call_args_list == [
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={"path": paths, "skip": "2", "take": "1"},
            ),
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={"path": paths, "skip": "3", "take": "1"},
            ),
        ]

        assert 2 == len(pages)
        assert 1 == len(pages[0])
        assert path1 == pages[0][0].path
        assert tbase.DataType.BOOLEAN == pages[0][0].data_type
        assert 1 == len(pages[1])
        assert path2 == pages[1][0].path
        assert tbase.DataType.DATE_TIME == pages[1][0].data_type

    def test__paths_with_keywords_and_properties_supplied__query__performs_query(self):
        total_count = 0
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"totalCount": total_count, "tags": []}]
            )
        )

        result = self._uut.query(
            ["tag1", "tag2"],
            ["keyword1", "keyword2"],
            OrderedDict((("prop1", "value1"), ("prop2", "value2"))),
        )

        assert total_count == result.total_count
        self._client.all_requests.assert_called_once_with(
            "GET",
            "/nitag/v2/tags",
            params={
                "path": "tag1,tag2",
                "keywords": "keyword1,keyword2",
                "properties": "prop1=value1,prop2=value2",
                "skip": "0",
            },
        )

    def test__only_keywords_and_properties_supplied__query__performs_query(self):
        total_count = 0
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"totalCount": total_count, "tags": []}]
            )
        )

        result = self._uut.query(
            None,
            ["keyword1", "keyword2"],
            OrderedDict((("prop1", "value1"), ("prop2", "value2"))),
        )

        assert total_count == result.total_count
        self._client.all_requests.assert_called_once_with(
            "GET",
            "/nitag/v2/tags",
            params={
                "keywords": "keyword1,keyword2",
                "properties": "prop1=value1,prop2=value2",
                "skip": "0",
            },
        )

    def test__all_inputs_supplied__query__performs_query(self):
        total_count = 4
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "BOOLEAN", "path": path1}],
                    },
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "DATE_TIME", "path": path2}],
                    },
                ]
            )
        )

        result = self._uut.query(
            ["missing1", path1, "missing2", path2, "missing3"],
            ["keyword1", "keyword2"],
            OrderedDict((("prop1", "value1"), ("prop2", "value2"))),
            skip=2,
            take=1,
        )
        assert total_count == result.total_count
        paths = ",".join(("missing1", path1, "missing2", path2, "missing3"))
        self._client.all_requests.assert_called_once_with(
            "GET",
            "/nitag/v2/tags",
            params={
                "path": paths,
                "keywords": "keyword1,keyword2",
                "properties": "prop1=value1,prop2=value2",
                "skip": "2",
                "take": "1",
            },
        )

        pages = list(result)
        assert self._client.all_requests.call_args_list == [
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={
                    "path": paths,
                    "keywords": "keyword1,keyword2",
                    "properties": "prop1=value1,prop2=value2",
                    "skip": "2",
                    "take": "1",
                },
            ),
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={
                    "path": paths,
                    "keywords": "keyword1,keyword2",
                    "properties": "prop1=value1,prop2=value2",
                    "skip": "3",
                    "take": "1",
                },
            ),
        ]

        assert 2 == len(pages)
        assert 1 == len(pages[0])
        assert path1 == pages[0][0].path
        assert tbase.DataType.BOOLEAN == pages[0][0].data_type
        assert 1 == len(pages[1])
        assert path2 == pages[1][0].path
        assert tbase.DataType.DATE_TIME == pages[1][0].data_type

    @pytest.mark.asyncio
    async def test__bad_arguments__query_async__raises(self):
        with pytest.raises(ValueError):
            await self._uut.query_async(skip=-1, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(skip=0, take=-1)

        with pytest.raises(ValueError):
            await self._uut.query_async([])
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", None])
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", ""])
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", " "])

        with pytest.raises(ValueError):
            await self._uut.query_async([], skip=0, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", None], skip=0, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", ""], skip=0, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", " "], skip=0, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag"], skip=-1, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag"], skip=0, take=-1)

        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", None], None, None)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", ""], None, None)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", " "], None, None)

        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", None], None, None, skip=0, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", ""], None, None, skip=0, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag", " "], None, None, skip=0, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag"], None, None, skip=-1, take=0)
        with pytest.raises(ValueError):
            await self._uut.query_async(["tag"], None, None, skip=0, take=-1)

    @pytest.mark.asyncio
    async def test__only_skip_and_take_supplied__query_async__performs_query(self):
        total_count = 4
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "BOOLEAN", "path": path1}],
                    },
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "DATE_TIME", "path": path2}],
                    },
                ]
            )
        )

        result = await self._uut.query_async(skip=2, take=1)

        assert total_count == result.total_count
        assert result.current_page is not None
        assert 1 == len(result.current_page)
        assert path1 == result.current_page[0].path
        assert tbase.DataType.BOOLEAN == result.current_page[0].data_type
        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"skip": "2", "take": "1"}
        )

        await result.move_next_page_async()

        assert result.current_page is not None
        assert 1 == len(result.current_page)
        assert path2 == result.current_page[0].path
        assert tbase.DataType.DATE_TIME == result.current_page[0].data_type
        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags", params={"skip": "2", "take": "1"}),
            mock.call("GET", "/nitag/v2/tags", params={"skip": "3", "take": "1"}),
        ]

        await result.move_next_page_async()

        assert result.current_page is None

    @pytest.mark.asyncio
    async def test__only_paths_supplied__query_async__performs_query(self):
        total_count = 0
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([{"totalCount": 0, "tags": []}])
        )

        result = await self._uut.query_async(["tag1", "tag2"])

        assert total_count == result.total_count
        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": "tag1,tag2", "skip": "0"}
        )

    @pytest.mark.asyncio
    async def test__path_with_skip_and_take_supplied__query_async__performs_query(self):
        total_count = 4
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "BOOLEAN", "path": path1}],
                    },
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "DATE_TIME", "path": path2}],
                    },
                ]
            )
        )

        result = await self._uut.query_async(
            ["missing1", path1, "missing2", path2, "missing3"], skip=2, take=1
        )

        assert total_count == result.total_count
        assert result.current_page is not None
        assert 1 == len(result.current_page)
        assert path1 == result.current_page[0].path
        assert tbase.DataType.BOOLEAN == result.current_page[0].data_type
        paths = ",".join(("missing1", path1, "missing2", path2, "missing3"))
        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags", params={"path": paths, "skip": "2", "take": "1"}
        )

        await result.move_next_page_async()

        assert result.current_page is not None
        assert 1 == len(result.current_page)
        assert path2 == result.current_page[0].path
        assert tbase.DataType.DATE_TIME == result.current_page[0].data_type
        assert self._client.all_requests.call_args_list == [
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={"path": paths, "skip": "2", "take": "1"},
            ),
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={"path": paths, "skip": "3", "take": "1"},
            ),
        ]

        await result.move_next_page_async()

        assert result.current_page is None

    @pytest.mark.asyncio
    async def test__paths_with_keywords_and_properties_supplied__query_async__performs_query(
        self,
    ):
        total_count = 0
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"totalCount": total_count, "tags": []}]
            )
        )

        result = await self._uut.query_async(
            ["tag1", "tag2"],
            ["keyword1", "keyword2"],
            OrderedDict((("prop1", "value1"), ("prop2", "value2"))),
        )

        assert total_count == result.total_count
        self._client.all_requests.assert_called_once_with(
            "GET",
            "/nitag/v2/tags",
            params={
                "path": "tag1,tag2",
                "keywords": "keyword1,keyword2",
                "properties": "prop1=value1,prop2=value2",
                "skip": "0",
            },
        )

    @pytest.mark.asyncio
    async def test__only_keywords_and_properties_supplied__query_async__performs_query(
        self,
    ):
        total_count = 0
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"totalCount": total_count, "tags": []}]
            )
        )

        result = await self._uut.query_async(
            None,
            ["keyword1", "keyword2"],
            OrderedDict((("prop1", "value1"), ("prop2", "value2"))),
        )

        assert total_count == result.total_count
        self._client.all_requests.assert_called_once_with(
            "GET",
            "/nitag/v2/tags",
            params={
                "keywords": "keyword1,keyword2",
                "properties": "prop1=value1,prop2=value2",
                "skip": "0",
            },
        )

    @pytest.mark.asyncio
    async def test__all_inputs_supplied__query_async__performs_query(self):
        total_count = 4
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "BOOLEAN", "path": path1}],
                    },
                    {
                        "totalCount": total_count,
                        "tags": [{"type": "DATE_TIME", "path": path2}],
                    },
                ]
            )
        )

        result = await self._uut.query_async(
            ["missing1", path1, "missing2", path2, "missing3"],
            ["keyword1", "keyword2"],
            OrderedDict((("prop1", "value1"), ("prop2", "value2"))),
            skip=2,
            take=1,
        )

        assert total_count == result.total_count
        assert result.current_page is not None
        assert 1 == len(result.current_page)
        assert path1 == result.current_page[0].path
        assert tbase.DataType.BOOLEAN == result.current_page[0].data_type
        paths = ",".join(("missing1", path1, "missing2", path2, "missing3"))
        self._client.all_requests.assert_called_once_with(
            "GET",
            "/nitag/v2/tags",
            params={
                "path": paths,
                "keywords": "keyword1,keyword2",
                "properties": "prop1=value1,prop2=value2",
                "skip": "2",
                "take": "1",
            },
        )

        await result.move_next_page_async()

        assert result.current_page is not None
        assert 1 == len(result.current_page)
        assert path2 == result.current_page[0].path
        assert tbase.DataType.DATE_TIME == result.current_page[0].data_type
        assert self._client.all_requests.call_args_list == [
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={
                    "path": paths,
                    "keywords": "keyword1,keyword2",
                    "properties": "prop1=value1,prop2=value2",
                    "skip": "2",
                    "take": "1",
                },
            ),
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={
                    "path": paths,
                    "keywords": "keyword1,keyword2",
                    "properties": "prop1=value1,prop2=value2",
                    "skip": "3",
                    "take": "1",
                },
            ),
        ]

        await result.move_next_page_async()

        assert result.current_page is None

    def test__bad_arguments__update_with_tags__raises(self):
        valid_tag = tbase.TagData("tag", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            self._uut.update(None)
        with pytest.raises(ValueError):
            self._uut.update([])
        with pytest.raises(ValueError):
            self._uut.update([valid_tag, None])
        with pytest.raises(ValueError):
            self._uut.update([valid_tag, tbase.TagData(None, tbase.DataType.BOOLEAN)])
        with pytest.raises(ValueError):
            self._uut.update([valid_tag, tbase.TagData("", tbase.DataType.BOOLEAN)])
        with pytest.raises(ValueError):
            self._uut.update([valid_tag, tbase.TagData(" ", tbase.DataType.BOOLEAN)])
        with pytest.raises(ValueError):
            self._uut.update([valid_tag, tbase.TagData("tag2", tbase.DataType.UNKNOWN)])

    def test__update_with_tags__metadata_sent_to_server(self):
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None])
        )
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        tag1 = tbase.TagData(path1, tbase.DataType.BOOLEAN, keywords, properties)
        tag1.set_retention_days(1)
        tag2 = tbase.TagData(path2, tbase.DataType.STRING)
        tag2.collect_aggregates = True
        all_properties1 = dict(properties)
        tag1._copy_retention_properties(all_properties1)
        all_properties2 = {}
        tag2._copy_retention_properties(all_properties2)

        self._uut.update([tag1, tag2])

        self._client.all_requests.assert_called_once_with(
            "POST",
            "/nitag/v2/update-tags",
            params=None,
            data={
                "tags": [
                    {
                        "path": path1,
                        "type": "BOOLEAN",
                        "keywords": keywords,
                        "properties": all_properties1,
                        "collectAggregates": False,
                    },
                    {
                        "path": path2,
                        "type": "STRING",
                        "properties": all_properties2,
                        "collectAggregates": True,
                    },
                ],
                "merge": False,
            },
        )

    def test__partial_success__update_with_tags__raises(self):
        path = "invalid"
        error = core.ApiError()
        error.name = "Tag.OneOrMoreErrorsOccurred"
        error.message = "One or more errors occurred"
        inner_errors = [core.ApiError(), core.ApiError()]
        inner_errors[0].name = "Tag.InvalidDataType"
        inner_errors[0].message = "Invalid data type"
        inner_errors[0].resource_type = "tag"
        inner_errors[0].resource_id = path
        inner_errors[1].name = "Tag.Conflict"
        inner_errors[1].message = "Conflict of some sort"
        inner_errors[1].resource_type = "tag"
        inner_errors[1].resource_id = "another"
        error.inner_errors = inner_errors
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "error": {
                            "name": error.name,
                            "message": error.message,
                            "innerErrors": [
                                {
                                    "name": error.inner_errors[0].name,
                                    "message": error.inner_errors[0].message,
                                    "resourceType": error.inner_errors[0].resource_type,
                                    "resourceId": error.inner_errors[0].resource_id,
                                },
                                {
                                    "name": error.inner_errors[1].name,
                                    "message": error.inner_errors[1].message,
                                    "resourceType": error.inner_errors[1].resource_type,
                                    "resourceId": error.inner_errors[1].resource_id,
                                },
                            ],
                        }
                    }
                ]
            )
        )

        with pytest.raises(core.ApiException) as ex:
            self._uut.update([tbase.TagData(path, tbase.DataType.BOOLEAN)])
        assert error == ex.value.error

    def test__bad_arguments__update_with_tag_updates__raises(self):
        validUpdate = tbase.TagDataUpdate.from_tagdata(
            tbase.TagData("tag", tbase.DataType.BOOLEAN), tbase.TagUpdateFields.ALL
        )
        with pytest.raises(ValueError):
            self._uut.update(None)
        with pytest.raises(ValueError):
            self._uut.update([])
        with pytest.raises(ValueError):
            self._uut.update([validUpdate, None])

        with pytest.raises(ValueError):
            self._uut.update(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData(None, tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

        with pytest.raises(ValueError):
            self._uut.update(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData("", tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

        with pytest.raises(ValueError):
            self._uut.update(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData(" ", tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

        with pytest.raises(ValueError):
            self._uut.update(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData("tag2", tbase.DataType.UNKNOWN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

    def test__update_with_tag_update__metadata_merge_sent_to_server(self):
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None])
        )
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        tag1 = tbase.TagData(path1, tbase.DataType.BOOLEAN, keywords, properties)
        tag1.set_retention_days(1)
        tag2 = tbase.TagData(path2, tbase.DataType.STRING)
        tag2.collect_aggregates = True
        all_properties2 = {}
        tag2._copy_retention_properties(all_properties2)

        self._uut.update(
            [
                tbase.TagDataUpdate.from_tagdata(
                    tag1, tbase.TagUpdateFields.PROPERTIES
                ),
                tbase.TagDataUpdate.from_tagdata(tag2, tbase.TagUpdateFields.ALL),
            ]
        )

        self._client.all_requests.assert_called_once_with(
            "POST",
            "/nitag/v2/update-tags",
            params=None,
            data={
                "tags": [
                    {"path": path1, "type": "BOOLEAN", "properties": properties},
                    {
                        "path": path2,
                        "type": "STRING",
                        "properties": all_properties2,
                        "collectAggregates": True,
                    },
                ],
                "merge": True,
            },
        )

    def test__partial_success__update_with_tag_updates__raises(self):
        path = "invalid"
        error = core.ApiError()
        error.name = ("Tag.OneOrMoreErrorsOccurred",)
        error.message = ("One or more errors occurred",)
        inner_errors = [core.ApiError(), core.ApiError()]
        inner_errors[0].name = ("Tag.InvalidDataType",)
        inner_errors[0].message = ("Invalid data type",)
        inner_errors[0].resource_type = ("tag",)
        inner_errors[0].resource_id = path
        inner_errors[1].name = ("Tag.Conflict",)
        inner_errors[1].message = ("Conflict of some sort",)
        inner_errors[1].resource_type = ("tag",)
        inner_errors[1].resource_id = "another"
        error.inner_errors = inner_errors
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "error": {
                            "name": error.name,
                            "message": error.message,
                            "innerErrors": [
                                {
                                    "name": error.inner_errors[0].name,
                                    "message": error.inner_errors[0].message,
                                    "resourceType": error.inner_errors[0].resource_type,
                                    "resourceId": error.inner_errors[0].resource_id,
                                },
                                {
                                    "name": error.inner_errors[1].name,
                                    "message": error.inner_errors[1].message,
                                    "resourceType": error.inner_errors[1].resource_type,
                                    "resourceId": error.inner_errors[1].resource_id,
                                },
                            ],
                        }
                    }
                ]
            )
        )

        with pytest.raises(core.ApiException) as ex:
            self._uut.update(
                [
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData(path, tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    )
                ]
            )
        assert error == ex.value.error

    @pytest.mark.asyncio
    async def test__bad_arguments__update_async_with_tags__raises(self):
        valid_tag = tbase.TagData("tag", tbase.DataType.BOOLEAN)
        with pytest.raises(ValueError):
            await self._uut.update_async(None)
        with pytest.raises(ValueError):
            await self._uut.update_async([])
        with pytest.raises(ValueError):
            await self._uut.update_async([valid_tag, None])
        with pytest.raises(ValueError):
            await self._uut.update_async(
                [valid_tag, tbase.TagData(None, tbase.DataType.BOOLEAN)]
            )
        with pytest.raises(ValueError):
            await self._uut.update_async(
                [valid_tag, tbase.TagData("", tbase.DataType.BOOLEAN)]
            )
        with pytest.raises(ValueError):
            await self._uut.update_async(
                [valid_tag, tbase.TagData(" ", tbase.DataType.BOOLEAN)]
            )
        with pytest.raises(ValueError):
            await self._uut.update_async(
                [valid_tag, tbase.TagData("tag2", tbase.DataType.UNKNOWN)]
            )

    @pytest.mark.asyncio
    async def test__update_async_with_tags__metadata_sent_to_server(self):
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None])
        )
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        tag1 = tbase.TagData(path1, tbase.DataType.BOOLEAN, keywords, properties)
        tag1.set_retention_days(1)
        tag2 = tbase.TagData(path2, tbase.DataType.STRING)
        tag2.collect_aggregates = True
        all_properties1 = dict(properties)
        tag1._copy_retention_properties(all_properties1)
        all_properties2 = {}
        tag2._copy_retention_properties(all_properties2)

        await self._uut.update_async([tag1, tag2])

        self._client.all_requests.assert_called_once_with(
            "POST",
            "/nitag/v2/update-tags",
            params=None,
            data={
                "tags": [
                    {
                        "path": path1,
                        "type": "BOOLEAN",
                        "keywords": keywords,
                        "properties": all_properties1,
                        "collectAggregates": False,
                    },
                    {
                        "path": path2,
                        "type": "STRING",
                        "properties": all_properties2,
                        "collectAggregates": True,
                    },
                ],
                "merge": False,
            },
        )

    @pytest.mark.asyncio
    async def test__partial_success__update_async_with_tags__raises(self):
        path = "invalid"
        error = core.ApiError()
        error.name = ("Tag.OneOrMoreErrorsOccurred",)
        error.message = ("One or more errors occurred",)
        inner_errors = [core.ApiError(), core.ApiError()]
        inner_errors[0].name = ("Tag.InvalidDataType",)
        inner_errors[0].message = ("Invalid data type",)
        inner_errors[0].resource_type = ("tag",)
        inner_errors[0].resource_id = path
        inner_errors[1].name = ("Tag.Conflict",)
        inner_errors[1].message = ("Conflict of some sort",)
        inner_errors[1].resource_type = ("tag",)
        inner_errors[1].resource_id = "another"
        error.inner_errors = inner_errors
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "error": {
                            "name": error.name,
                            "message": error.message,
                            "innerErrors": [
                                {
                                    "name": error.inner_errors[0].name,
                                    "message": error.inner_errors[0].message,
                                    "resourceType": error.inner_errors[0].resource_type,
                                    "resourceId": error.inner_errors[0].resource_id,
                                },
                                {
                                    "name": error.inner_errors[1].name,
                                    "message": error.inner_errors[1].message,
                                    "resourceType": error.inner_errors[1].resource_type,
                                    "resourceId": error.inner_errors[1].resource_id,
                                },
                            ],
                        }
                    }
                ]
            )
        )

        with pytest.raises(core.ApiException) as ex:
            await self._uut.update_async([tbase.TagData(path, tbase.DataType.BOOLEAN)])
        assert error == ex.value.error

    @pytest.mark.asyncio
    async def test__bad_arguments__update_async_with_tag_updates__raises(self):
        validUpdate = tbase.TagDataUpdate.from_tagdata(
            tbase.TagData("tag", tbase.DataType.BOOLEAN), tbase.TagUpdateFields.ALL
        )
        with pytest.raises(ValueError):
            await self._uut.update_async(None)
        with pytest.raises(ValueError):
            await self._uut.update_async([])
        with pytest.raises(ValueError):
            await self._uut.update_async([validUpdate, None])

        with pytest.raises(ValueError):
            await self._uut.update_async(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData(None, tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

        with pytest.raises(ValueError):
            await self._uut.update_async(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData("", tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

        with pytest.raises(ValueError):
            await self._uut.update_async(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData(" ", tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

        with pytest.raises(ValueError):
            await self._uut.update_async(
                [
                    validUpdate,
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData("tag2", tbase.DataType.UNKNOWN),
                        tbase.TagUpdateFields.ALL,
                    ),
                ]
            )

    @pytest.mark.asyncio
    async def test__update_async_with_tag_update__metadata_merge_sent_to_server(self):
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None])
        )
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        tag1 = tbase.TagData(path1, tbase.DataType.BOOLEAN, keywords, properties)
        tag1.set_retention_days(1)
        tag2 = tbase.TagData(path2, tbase.DataType.STRING)
        tag2.collect_aggregates = True
        all_properties2 = {}
        tag2._copy_retention_properties(all_properties2)

        await self._uut.update_async(
            [
                tbase.TagDataUpdate.from_tagdata(
                    tag1, tbase.TagUpdateFields.PROPERTIES
                ),
                tbase.TagDataUpdate.from_tagdata(tag2, tbase.TagUpdateFields.ALL),
            ]
        )

        self._client.all_requests.assert_called_once_with(
            "POST",
            "/nitag/v2/update-tags",
            params=None,
            data={
                "tags": [
                    {"path": path1, "type": "BOOLEAN", "properties": properties},
                    {
                        "path": path2,
                        "type": "STRING",
                        "properties": all_properties2,
                        "collectAggregates": True,
                    },
                ],
                "merge": True,
            },
        )

    @pytest.mark.asyncio
    async def test__partial_success__update_async_with_tag_updates__raises(self):
        path = "invalid"
        error = core.ApiError()
        error.name = ("Tag.OneOrMoreErrorsOccurred",)
        error.message = ("One or more errors occurred",)
        inner_errors = [core.ApiError(), core.ApiError()]
        inner_errors[0].name = ("Tag.InvalidDataType",)
        inner_errors[0].message = ("Invalid data type",)
        inner_errors[0].resource_type = ("tag",)
        inner_errors[0].resource_id = path
        inner_errors[1].name = ("Tag.Conflict",)
        inner_errors[1].message = ("Conflict of some sort",)
        inner_errors[1].resource_type = ("tag",)
        inner_errors[1].resource_id = "another"
        error.inner_errors = inner_errors
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "error": {
                            "name": error.name,
                            "message": error.message,
                            "innerErrors": [
                                {
                                    "name": error.inner_errors[0].name,
                                    "message": error.inner_errors[0].message,
                                    "resourceType": error.inner_errors[0].resource_type,
                                    "resourceId": error.inner_errors[0].resource_id,
                                },
                                {
                                    "name": error.inner_errors[1].name,
                                    "message": error.inner_errors[1].message,
                                    "resourceType": error.inner_errors[1].resource_type,
                                    "resourceId": error.inner_errors[1].resource_id,
                                },
                            ],
                        }
                    }
                ]
            )
        )

        with pytest.raises(core.ApiException) as ex:
            await self._uut.update_async(
                [
                    tbase.TagDataUpdate.from_tagdata(
                        tbase.TagData(path, tbase.DataType.BOOLEAN),
                        tbase.TagUpdateFields.ALL,
                    )
                ]
            )
        assert error == ex.value.error

    def test__bad_arguments__delete_tags__raises(self):
        with pytest.raises(ValueError):
            self._uut.delete(None)
        with pytest.raises(ValueError):
            self._uut.delete([tbase.TagData("tag"), None])
        with pytest.raises(ValueError):
            self._uut.delete([tbase.TagData("tag"), tbase.TagData(None)])
        with pytest.raises(ValueError):
            self._uut.delete([tbase.TagData("tag"), tbase.TagData("")])
        with pytest.raises(ValueError):
            self._uut.delete([tbase.TagData("tag"), tbase.TagData(" ")])
        with pytest.raises(ValueError):
            self._uut.delete([tbase.TagData("tag"), tbase.TagData("*")])

    def test__delete_tags__deletes_using_paths(self):
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None, None])
        )
        self._uut.delete(
            [tbase.TagData(path1, tbase.DataType.STRING), tbase.TagData(path2)]
        )

        assert self._client.all_requests.call_args_list == [
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2}),
        ]

    def test__bad_arguments__delete_paths__raises(self):
        with pytest.raises(ValueError):
            self._uut.delete(None)
        with pytest.raises(ValueError):
            self._uut.delete(["tag", None])
        with pytest.raises(ValueError):
            self._uut.delete(["tag", ""])
        with pytest.raises(ValueError):
            self._uut.delete(["tag", " "])
        with pytest.raises(ValueError):
            self._uut.delete(["tag", "*"])

    def test__empty_list__delete_paths__api_not_called(self):
        self._uut.delete([])

        assert self._client.all_requests.call_count == 0

    def test__small_number_of_paths__delete_paths__separate_deletes_sent_to_server(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None] * 6)
        )

        self._uut.delete([path1])
        self._uut.delete([path1, path2])
        self._uut.delete([path1, path2, path3])

        assert self._client.all_requests.call_args_list == [
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path3}),
        ]

    def test__server_error_with_small_number_of_paths__delete_paths__raises_first_exception(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        deleteException = core.ApiException("oops")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    # tag1
                    deleteException,
                    # tag1, tag2
                    None,
                    deleteException,
                    # tag1, tag2, tag3
                    deleteException,
                    deleteException,
                    deleteException,
                ]
            )
        )

        with pytest.raises(core.ApiException) as ex:
            self._uut.delete([path1])
        assert deleteException is ex.value
        with pytest.raises(core.ApiException) as ex:
            self._uut.delete([path1, path2])
        assert deleteException is ex.value
        with pytest.raises(core.ApiException) as ex:
            self._uut.delete([path1, path2, path3])
        assert deleteException is ex.value

        assert self._client.all_requests.call_args_list == [
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2}),
            mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path3}),
        ]

    def test__many_paths__delete_paths__temporary_selection_used_for_delete(self):
        token = "selection for delete"
        paths = ["tag1", "tag2", "tag3", "tag4"]

        def mock_request(method, uri, data=None, **kwargs):
            if data is not None:
                return (
                    {"id": token, "searchPaths": data.get("searchPaths")},
                    MockResponse(method, uri),
                )
            else:
                return None, MockResponse(method, uri)

        self._client.all_requests.configure_mock(side_effect=mock_request)

        self._uut.delete(paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    def test__server_error_with_many_paths__delete_paths__raises(self):
        token = "selection for delete"
        paths = ["tag1", "tag2", "tag3", "tag4"]
        createException = core.ApiException("can't create")
        deleteException = core.ApiException("can't delete")
        self._client.all_requests.configure_mock(side_effect=createException)

        with pytest.raises(core.ApiException) as ex:
            self._uut.delete(paths)

        assert createException is ex.value

        # ===

        def mock_request(method, uri, data=None, **kwargs):
            if data is not None:
                return (
                    {"id": token, "searchPaths": data.get("searchPaths")},
                    MockResponse(method, uri),
                )
            elif method == "DELETE":
                if uri.endswith("/tags"):
                    raise deleteException
                else:
                    return None, MockResponse(method, uri)
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        with pytest.raises(core.ApiException) as ex:
            self._uut.delete(paths)

        assert deleteException is ex.value
        assert self._client.all_requests.call_args_list == [
            # From the first attempt
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            # From the second attempt
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    def test__server_error_when_deleting_temp_selection__delete_paths__error_ignored(
        self,
    ):
        token = "selection for delete"
        paths = ["tag1", "tag2", "tag3", "tag4"]

        def mock_request(method, uri, data=None, **kwargs):
            if data is not None:
                return (
                    {"id": token, "searchPaths": data.get("searchPaths")},
                    MockResponse(method, uri),
                )
            elif method == "DELETE":
                if not uri.endswith("/tags"):
                    raise core.ApiException("can't delete selection")
                else:
                    return None, MockResponse(method, uri)
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        self._uut.delete(paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__bad_arguments__delete_tags_async__raises(self):
        with pytest.raises(ValueError):
            await self._uut.delete_async(None)
        with pytest.raises(ValueError):
            await self._uut.delete_async([tbase.TagData("tag"), None])
        with pytest.raises(ValueError):
            await self._uut.delete_async([tbase.TagData("tag"), tbase.TagData(None)])
        with pytest.raises(ValueError):
            await self._uut.delete_async([tbase.TagData("tag"), tbase.TagData("")])
        with pytest.raises(ValueError):
            await self._uut.delete_async([tbase.TagData("tag"), tbase.TagData(" ")])
        with pytest.raises(ValueError):
            await self._uut.delete_async([tbase.TagData("tag"), tbase.TagData("*")])

    @pytest.mark.asyncio
    async def test__delete_tags_async__deletes_using_paths(self):
        path1 = "tag1"
        path2 = "tag2"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None, None])
        )
        await self._uut.delete_async(
            [tbase.TagData(path1, tbase.DataType.STRING), tbase.TagData(path2)]
        )

        assert sorted(str(c) for c in self._client.all_requests.call_args_list) == [
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2})),
        ]

    @pytest.mark.asyncio
    async def test__bad_arguments__delete_paths_async__raises(self):
        with pytest.raises(ValueError):
            await self._uut.delete_async(None)
        with pytest.raises(ValueError):
            await self._uut.delete_async(["tag", None])
        with pytest.raises(ValueError):
            await self._uut.delete_async(["tag", ""])
        with pytest.raises(ValueError):
            await self._uut.delete_async(["tag", " "])
        with pytest.raises(ValueError):
            await self._uut.delete_async(["tag", "*"])

    @pytest.mark.asyncio
    async def test__empty_list__delete_paths_async__api_not_called(self):
        await self._uut.delete_async([])

        assert self._client.all_requests.call_count == 0

    @pytest.mark.asyncio
    async def test__small_number_of_paths__delete_paths_async__separate_deletes_sent_to_server(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None] * 6)
        )

        await asyncio.gather(
            self._uut.delete_async([path1]),
            self._uut.delete_async([path1, path2]),
            self._uut.delete_async([path1, path2, path3]),
        )

        assert sorted(str(c) for c in self._client.all_requests.call_args_list) == [
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path3})),
        ]

    @pytest.mark.asyncio
    async def test__server_error_with_small_number_of_paths__delete_paths_async__raises_first_exception(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        deleteException = core.ApiException("oops")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    # tag1
                    deleteException,
                    # tag1, tag2
                    None,
                    deleteException,
                    # tag1, tag2, tag3
                    deleteException,
                    deleteException,
                    deleteException,
                ]
            )
        )

        with pytest.raises(core.ApiException) as ex:
            await self._uut.delete_async([path1])
        assert deleteException is ex.value
        with pytest.raises(core.ApiException) as ex:
            await self._uut.delete_async([path1, path2])
        assert deleteException is ex.value
        with pytest.raises(core.ApiException) as ex:
            await self._uut.delete_async([path1, path2, path3])
        assert deleteException is ex.value

        assert sorted(str(c) for c in self._client.all_requests.call_args_list) == [
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path1})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path2})),
            str(mock.call("DELETE", "/nitag/v2/tags/{path}", params={"path": path3})),
        ]

    @pytest.mark.asyncio
    async def test__many_paths__delete_paths_async__temporary_selection_used_for_delete(
        self,
    ):
        token = "selection for delete"
        paths = ["tag1", "tag2", "tag3", "tag4"]

        def mock_request(method, uri, data=None, **kwargs):
            if data is not None:
                return (
                    {"id": token, "searchPaths": data.get("searchPaths")},
                    MockResponse(method, uri),
                )
            else:
                return None, MockResponse(method, uri)

        self._client.all_requests.configure_mock(side_effect=mock_request)

        await self._uut.delete_async(paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__server_error_with_many_paths__delete_paths_async__raises(self):
        token = "selection for delete"
        paths = ["tag1", "tag2", "tag3", "tag4"]
        createException = core.ApiException("can't create")
        deleteException = core.ApiException("can't delete")
        self._client.all_requests.configure_mock(side_effect=createException)

        with pytest.raises(core.ApiException) as ex:
            await self._uut.delete_async(paths)

        assert createException is ex.value

        # ===

        def mock_request(method, uri, data=None, **kwargs):
            if data is not None:
                return (
                    {"id": token, "searchPaths": data.get("searchPaths")},
                    MockResponse(method, uri),
                )
            elif method == "DELETE":
                if uri.endswith("/tags"):
                    raise deleteException
                else:
                    return None, MockResponse(method, uri)
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        with pytest.raises(core.ApiException) as ex:
            await self._uut.delete_async(paths)

        assert deleteException is ex.value
        assert self._client.all_requests.call_args_list == [
            # From the first attempt
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            # From the second attempt
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__server_error_when_deleting_temp_selection__delete_paths_async__error_ignored(
        self,
    ):
        token = "selection for delete"
        paths = ["tag1", "tag2", "tag3", "tag4"]

        def mock_request(method, uri, data=None, **kwargs):
            if data is not None:
                return (
                    {"id": token, "searchPaths": data.get("searchPaths")},
                    MockResponse(method, uri),
                )
            elif method == "DELETE":
                if not uri.endswith("/tags"):
                    raise core.ApiException("can't delete selection")
                else:
                    return None, MockResponse(method, uri)
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        await self._uut.delete_async(paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": paths, "inactivityTimeout": 30},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    def test__bad_arguments__create_writer__raises(self):
        with pytest.raises(ValueError):
            self._uut.create_writer(buffer_size=0)
        with pytest.raises(ValueError):
            self._uut.create_writer(max_buffer_time=timedelta(0))
        with pytest.raises(ValueError):
            self._uut.create_writer(buffer_size=0, max_buffer_time=timedelta(minutes=1))
        with pytest.raises(ValueError):
            self._uut.create_writer(buffer_size=1, max_buffer_time=timedelta(0))

    def test__create_writer_with_buffer_size__sends_when_buffer_full(self):
        path = "tag"
        value1 = 1
        value2 = 2
        writer = self._uut.create_writer(buffer_size=2)
        timestamp = datetime.now()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None])
        )

        writer.write(path, tbase.DataType.INT32, value1, timestamp=timestamp)
        writer.write(path, tbase.DataType.INT32, value2, timestamp=timestamp)

        utctime = datetime.utcfromtimestamp(timestamp.timestamp()).isoformat() + "Z"
        self._client.all_requests.assert_called_once_with(
            "POST",
            "/nitag/v2/update-current-values",
            params=None,
            data=[
                {
                    "path": path,
                    "updates": [
                        {
                            "value": {"type": "INT", "value": str(value1)},
                            "timestamp": utctime,
                        },
                        {
                            "value": {"type": "INT", "value": str(value2)},
                            "timestamp": utctime,
                        },
                    ],
                },
            ],
        )

    def test__create_writer_with_buffer_time__sends_when_timer_elapsed(self):
        path = "tag"
        value = 1
        writer = self._uut.create_writer(max_buffer_time=timedelta(milliseconds=50))
        timestamp = datetime.now()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None])
        )

        writer.write(path, tbase.DataType.INT32, value, timestamp=timestamp)
        self._client.all_requests.assert_not_called()
        for i in range(100):
            if self._client.all_requests.call_count > 0:
                break
            time.sleep(0.01)

        utctime = datetime.utcfromtimestamp(timestamp.timestamp()).isoformat() + "Z"
        self._client.all_requests.assert_called_once_with(
            "POST",
            "/nitag/v2/update-current-values",
            params=None,
            data=[
                {
                    "path": path,
                    "updates": [
                        {
                            "value": {"type": "INT", "value": str(value)},
                            "timestamp": utctime,
                        }
                    ],
                }
            ],
        )

    def test__create_writer_with_buffer_size_and_timer__obeys_both_settings(self):
        path = "tag"
        value1 = 1
        value2 = 2
        value3 = 3
        writer1 = self._uut.create_writer(
            buffer_size=2, max_buffer_time=timedelta(minutes=1)
        )
        writer2 = self._uut.create_writer(
            buffer_size=2, max_buffer_time=timedelta(milliseconds=50)
        )
        timestamp = datetime.now()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None, None])
        )

        writer1.write(path, tbase.DataType.INT32, value1, timestamp=timestamp)
        writer1.write(path, tbase.DataType.INT32, value2, timestamp=timestamp)

        utctime = datetime.utcfromtimestamp(timestamp.timestamp()).isoformat() + "Z"
        self._client.all_requests.assert_called_once_with(
            "POST",
            "/nitag/v2/update-current-values",
            params=None,
            data=[
                {
                    "path": path,
                    "updates": [
                        {
                            "value": {"type": "INT", "value": str(value1)},
                            "timestamp": utctime,
                        },
                        {
                            "value": {"type": "INT", "value": str(value2)},
                            "timestamp": utctime,
                        },
                    ],
                }
            ],
        )

        writer2.write(path, tbase.DataType.INT32, value3, timestamp=timestamp)
        assert 1 == self._client.all_requests.call_count  # same as before
        for i in range(100):
            if self._client.all_requests.call_count > 1:
                break
            time.sleep(0.01)

        assert 2 == self._client.all_requests.call_count
        assert self._client.all_requests.call_args_list[1] == mock.call(
            "POST",
            "/nitag/v2/update-current-values",
            params=None,
            data=[
                {
                    "path": path,
                    "updates": [
                        {
                            "value": {"type": "INT", "value": str(value3)},
                            "timestamp": utctime,
                        }
                    ],
                }
            ],
        )

    def test__bad_arguments__read__raises(self):
        with pytest.raises(ValueError):
            self._uut.read(None, include_timestamp=True, include_aggregates=True)
        with pytest.raises(ValueError):
            self._uut.read("", include_timestamp=True, include_aggregates=True)
        with pytest.raises(ValueError):
            self._uut.read(" ", include_timestamp=True, include_aggregates=True)
        with pytest.raises(ValueError):
            self._uut.read("*", include_timestamp=True, include_aggregates=True)

    def test__read_with_timestamp_and_aggregates__retrieves_all_data_from_server(self):
        path = "test"
        value = "success"
        now = datetime.now(timezone.utc)
        utctime = datetime.utcfromtimestamp(now.timestamp()).isoformat() + "Z"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "current": {
                            "value": {"type": "STRING", "value": value},
                            "timestamp": utctime,
                        },
                        "aggregates": {"count": 7},
                    }
                ]
            )
        )

        result = self._uut.read(path, include_timestamp=True, include_aggregates=True)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.STRING == result.data_type
        assert value == result.value
        assert now == result.timestamp
        assert 7 == result.count
        assert result.max is None
        assert result.min is None
        assert result.mean is None

    def test__read_with_aggregates__allows_missing_timestamp(self):
        path = "test"
        value = 3.14
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "current": {"value": {"type": "DOUBLE", "value": str(value)}},
                        "aggregates": {
                            "min": "-1.3",
                            "max": "8.9",
                            "count": 3,
                            "avg": 4.7,
                        },
                    }
                ]
            )
        )

        result = self._uut.read(path, include_timestamp=False, include_aggregates=True)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.DOUBLE == result.data_type
        assert value == result.value
        assert result.timestamp is None
        assert -1.3 == result.min
        assert 8.9 == result.max
        assert 3 == result.count
        assert 4.7 == result.mean

    def test__read_with_timestamp__does_not_query_aggregates(self):
        path = "test"
        value = "success"
        now = datetime.now(timezone.utc)
        utctime = datetime.utcfromtimestamp(now.timestamp()).isoformat() + "Z"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "current": {
                            "value": {"type": "STRING", "value": value},
                            "timestamp": utctime,
                        }
                    }
                ]
            )
        )

        result = self._uut.read(path, include_timestamp=True, include_aggregates=False)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values/current", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.STRING == result.data_type
        assert value == result.value
        assert now == result.timestamp
        assert result.count is None
        assert result.max is None
        assert result.min is None
        assert result.mean is None

    def test__read_without_timestamp__retrieves_minimal_data_from_server(self):
        path = "test"
        value = "success"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"current": {"value": {"type": "STRING", "value": value}}}]
            )
        )

        result = self._uut.read(path, include_timestamp=False, include_aggregates=False)

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values/current/value", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.STRING == result.data_type
        assert value == result.value
        assert result.timestamp is None
        assert result.count is None
        assert result.max is None
        assert result.min is None
        assert result.mean is None

    def test__no_tag_value__read__returns_None(self):
        path = "test"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None] * 4)
        )

        assert (
            self._uut.read(path, include_timestamp=True, include_aggregates=True)
            is None
        )
        assert (
            self._uut.read(path, include_timestamp=False, include_aggregates=True)
            is None
        )
        assert (
            self._uut.read(path, include_timestamp=True, include_aggregates=False)
            is None
        )
        assert (
            self._uut.read(path, include_timestamp=False, include_aggregates=False)
            is None
        )

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}/values", params={"path": path}),
            mock.call("GET", "/nitag/v2/tags/{path}/values", params={"path": path}),
            mock.call(
                "GET", "/nitag/v2/tags/{path}/values/current", params={"path": path}
            ),
            mock.call(
                "GET",
                "/nitag/v2/tags/{path}/values/current/value",
                params={"path": path},
            ),
        ]

    @pytest.mark.asyncio
    async def test__bad_arguments__read_async__raises(self):
        with pytest.raises(ValueError):
            await self._uut.read_async(
                None, include_timestamp=True, include_aggregates=True
            )
        with pytest.raises(ValueError):
            await self._uut.read_async(
                "", include_timestamp=True, include_aggregates=True
            )
        with pytest.raises(ValueError):
            await self._uut.read_async(
                " ", include_timestamp=True, include_aggregates=True
            )
        with pytest.raises(ValueError):
            await self._uut.read_async(
                "*", include_timestamp=True, include_aggregates=True
            )

    @pytest.mark.asyncio
    async def test__read_async_with_timestamp_and_aggregates__retrieves_all_data_from_server(
        self,
    ):
        path = "test"
        value = "success"
        now = datetime.now(timezone.utc)
        utctime = datetime.utcfromtimestamp(now.timestamp()).isoformat() + "Z"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "current": {
                            "value": {"type": "STRING", "value": value},
                            "timestamp": utctime,
                        },
                        "aggregates": {"count": 7},
                    }
                ]
            )
        )

        result = await self._uut.read_async(
            path, include_timestamp=True, include_aggregates=True
        )

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.STRING == result.data_type
        assert value == result.value
        assert now == result.timestamp
        assert 7 == result.count
        assert result.max is None
        assert result.min is None
        assert result.mean is None

    @pytest.mark.asyncio
    async def test__read_async_with_aggregates__allows_missing_timestamp(self):
        path = "test"
        value = 3.14
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "current": {"value": {"type": "DOUBLE", "value": value}},
                        "aggregates": {
                            "min": "-1.3",
                            "max": "8.9",
                            "count": 3,
                            "avg": 4.7,
                        },
                    }
                ]
            )
        )

        result = await self._uut.read_async(
            path, include_timestamp=False, include_aggregates=True
        )

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.DOUBLE == result.data_type
        assert value == result.value
        assert result.timestamp is None
        assert -1.3 == result.min
        assert 8.9 == result.max
        assert 3 == result.count
        assert 4.7 == result.mean

    @pytest.mark.asyncio
    async def test__read_async_with_timestamp__does_not_query_aggregates(self):
        path = "test"
        value = "success"
        now = datetime.now(timezone.utc)
        utctime = datetime.utcfromtimestamp(now.timestamp()).isoformat() + "Z"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "current": {
                            "value": {"type": "STRING", "value": value},
                            "timestamp": utctime,
                        }
                    }
                ]
            )
        )

        result = await self._uut.read_async(
            path, include_timestamp=True, include_aggregates=False
        )

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values/current", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.STRING == result.data_type
        assert value == result.value
        assert now == result.timestamp
        assert result.count is None
        assert result.max is None
        assert result.min is None
        assert result.mean is None

    @pytest.mark.asyncio
    async def test__read_async_without_timestamp__retrieves_minimal_data_from_server(
        self,
    ):
        path = "test"
        value = "success"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [{"current": {"value": {"type": "STRING", "value": value}}}]
            )
        )

        result = await self._uut.read_async(
            path, include_timestamp=False, include_aggregates=False
        )

        self._client.all_requests.assert_called_once_with(
            "GET", "/nitag/v2/tags/{path}/values/current/value", params={"path": path}
        )
        assert result is not None
        assert path == result.path
        assert tbase.DataType.STRING == result.data_type
        assert value == result.value
        assert result.timestamp is None
        assert result.count is None
        assert result.max is None
        assert result.min is None
        assert result.mean is None

    @pytest.mark.asyncio
    async def test__no_tag_value__read_async__returns_None(self):
        path = "test"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([None] * 4)
        )

        assert (
            await self._uut.read_async(
                path, include_timestamp=True, include_aggregates=True
            )
            is None
        )
        assert (
            await self._uut.read_async(
                path, include_timestamp=False, include_aggregates=True
            )
            is None
        )
        assert (
            await self._uut.read_async(
                path, include_timestamp=True, include_aggregates=False
            )
            is None
        )
        assert (
            await self._uut.read_async(
                path, include_timestamp=False, include_aggregates=False
            )
            is None
        )

        assert self._client.all_requests.call_args_list == [
            mock.call("GET", "/nitag/v2/tags/{path}/values", params={"path": path}),
            mock.call("GET", "/nitag/v2/tags/{path}/values", params={"path": path}),
            mock.call(
                "GET", "/nitag/v2/tags/{path}/values/current", params={"path": path}
            ),
            mock.call(
                "GET",
                "/nitag/v2/tags/{path}/values/current/value",
                params={"path": path},
            ),
        ]
