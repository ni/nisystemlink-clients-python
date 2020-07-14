import uuid
from datetime import datetime, timezone
from unittest import mock

import pytest  # type: ignore
from systemlink.clients import core, tag as tbase
from systemlink.clients.tag._http._http_tag_selection import HttpTagSelection

from .httpclienttestbase import HttpClientTestBase, MockResponse
from ...anyorderlist import AnyOrderList


class TestHttpTagSelection(HttpClientTestBase):
    @classmethod
    def _get_mock_request(cls, token, query_result, values_result=None):
        # Override the parent class's implementation with a more specific one

        def mock_request(method, uri, params=None, data=None):
            if method == "DELETE":
                ret = None
            elif uri.startswith("/nitag/v2/selections"):
                if uri in ("/nitag/v2/selections", "/nitag/v2/selections/{id}",):
                    data = dict(data)
                    data.update({"id": token})
                    ret = data
                elif uri.endswith("/tags"):
                    if isinstance(query_result, Exception):
                        raise query_result
                    else:
                        ret = query_result
                elif values_result is not None and uri.endswith("values"):
                    ret = values_result
                elif uri.endswith("/reset-aggregates"):
                    ret = None
                else:
                    assert False, uri
            elif uri.startswith("/nitag/v2/subscriptions"):
                if uri == "/nitag/v2/subscriptions":
                    ret = {"subscriptionId": token}
                elif uri.endswith("/values/current"):
                    if isinstance(query_result, Exception):
                        raise query_result
                    else:
                        ret = query_result
                else:
                    assert False, uri
            else:
                assert False, uri

            return ret, MockResponse(method, uri)

        return mock_request

    def test__metadata_supplied__constructed__no_server_queries(self):
        tags = [tbase.TagData("tag", tbase.DataType.BOOLEAN)]
        uut = HttpTagSelection(self._client, tags)
        assert tags == list(uut.metadata.values())
        assert self._client.all_requests.call_count == 0

    def test__open__creates_selection_and_loads_all_data_from_server(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        public_properties = {
            "prop1": "value1",
            "prop2": "value2",
        }
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path1)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        tags = [
            {
                "path": path1,
                "type": "BOOLEAN",
                "keywords": keywords,
                "properties": all_properties,
                "collectAggregates": True,
            },
            {"path": path2, "type": "DOUBLE"},
        ]
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = HttpTagSelection.open(self._client, paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]
        assert 2 == len(uut.metadata)
        assert tbase.DataType.BOOLEAN == uut.metadata[path1].data_type
        assert uut.metadata[path1].collect_aggregates is True
        assert keywords == sorted(uut.metadata[path1].keywords)
        assert sorted(public_properties.items()) == sorted(
            uut.metadata[path1].properties.items()
        )
        assert dummy_tag.retention_count == uut.metadata[path1].retention_count
        assert dummy_tag.retention_days == uut.metadata[path1].retention_days
        assert dummy_tag.retention_type == uut.metadata[path1].retention_type

        assert tbase.DataType.DOUBLE == uut.metadata[path2].data_type
        assert uut.metadata[path2].collect_aggregates is False
        assert 0 == len(uut.metadata[path2].keywords)
        assert 0 == len(uut.metadata[path2].properties)
        assert uut.metadata[path2].retention_count is None
        assert uut.metadata[path2].retention_days is None
        assert tbase.RetentionType.NONE == uut.metadata[path2].retention_type

    @pytest.mark.asyncio
    async def test__open_async__creates_selection_and_loads_all_data_from_api(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        public_properties = {
            "prop1": "value1",
            "prop2": "value2",
        }
        all_properties = dict(public_properties)
        dummy_tag = tbase.TagData(path1)
        dummy_tag.retention_type = tbase.RetentionType.COUNT
        dummy_tag.retention_count = 7
        dummy_tag.retention_days = 9
        dummy_tag._copy_retention_properties(all_properties)
        keywords = ["keyword1", "keyword2"]
        tags = [
            {
                "path": path1,
                "type": "BOOLEAN",
                "keywords": keywords,
                "properties": all_properties,
                "collectAggregates": True,
            },
            {"path": path2, "type": "DOUBLE"},
        ]
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = await HttpTagSelection.open_async(self._client, paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]
        assert 2 == len(uut.metadata)
        assert tbase.DataType.BOOLEAN == uut.metadata[path1].data_type
        assert uut.metadata[path1].collect_aggregates is True
        assert keywords == sorted(uut.metadata[path1].keywords)
        assert sorted(public_properties.items()) == sorted(
            uut.metadata[path1].properties.items()
        )
        assert dummy_tag.retention_count == uut.metadata[path1].retention_count
        assert dummy_tag.retention_days == uut.metadata[path1].retention_days
        assert dummy_tag.retention_type == uut.metadata[path1].retention_type

        assert tbase.DataType.DOUBLE == uut.metadata[path2].data_type
        assert uut.metadata[path2].collect_aggregates is False
        assert 0 == len(uut.metadata[path2].keywords)
        assert 0 == len(uut.metadata[path2].properties)
        assert uut.metadata[path2].retention_count is None
        assert uut.metadata[path2].retention_days is None
        assert tbase.RetentionType.NONE == uut.metadata[path2].retention_type

    def test__error_on_tag_query__open__selection_deleted(self):
        paths = ["path"]
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, core.ApiException("Oops"))
        )

        with pytest.raises(core.ApiException):
            HttpTagSelection.open(self._client, paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__error_on_tag_query__open_async__selection_deleted(self):
        paths = ["path"]
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, core.ApiException("Oops"))
        )

        with pytest.raises(core.ApiException):
            await HttpTagSelection.open_async(self._client, paths)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__close__selection_deleted(self):
        paths = ["path"]
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, [])
        )

        uut = await HttpTagSelection.open_async(self._client, paths)
        uut.close()
        uut.close()
        await uut.close_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__close_async__selection_deleted(self):
        paths = ["path"]
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, [])
        )

        uut = await HttpTagSelection.open_async(self._client, paths)
        await uut.close_async()
        await uut.close_async()
        uut.close()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__no_selection_created_by_constructor__close__no_server_calls(self):
        uut = HttpTagSelection(self._client, [tbase.TagData("tag")])
        uut.close()
        uut.close()
        await uut.close_async()
        assert self._client.all_requests.call_count == 0

    @pytest.mark.asyncio
    async def test__no_selection_created_by_constructor__close_async__no_server_calls(
        self,
    ):
        uut = HttpTagSelection(self._client, [tbase.TagData("tag")])
        await uut.close_async()
        await uut.close_async()
        uut.close()
        assert self._client.all_requests.call_count == 0

    def test__create_subscription__subscription_created_with_paths(self):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {"subscriptionUpdates": []})
        )
        uut = HttpTagSelection(
            self._client, [tbase.TagData(path1), tbase.TagData(path2)]
        )

        with uut.create_subscription():
            pass

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/subscriptions",
                params=None,
                data={"tags": AnyOrderList([path1, path2]), "updatesOnly": True},
            ),
            mock.call(
                "GET",
                "/nitag/v2/subscriptions/{id}/values/current",
                params={"id": token},
            ),
            mock.call("DELETE", "/nitag/v2/subscriptions/{id}", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__create_subscription_async__subscription_created_with_paths(self,):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {"subscriptionUpdates": []})
        )
        uut = HttpTagSelection(
            self._client, [tbase.TagData(path1), tbase.TagData(path2)]
        )

        async with await uut.create_subscription_async():
            pass

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/subscriptions",
                params=None,
                data={"tags": AnyOrderList([path1, path2]), "updatesOnly": True},
            ),
            mock.call(
                "GET",
                "/nitag/v2/subscriptions/{id}/values/current",
                params={"id": token},
            ),
            mock.call("DELETE", "/nitag/v2/subscriptions/{id}", params={"id": token}),
        ]

    def test__no_selection_created_by_constructor__api_function_called__selection_created(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, AssertionError())
        )

        uut = HttpTagSelection(
            self._client, [tbase.TagData(path1), tbase.TagData(path2)]
        )
        uut.delete_tags_from_server()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    def test__selection_created_by_constructor__api_function_called__selection_reused(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = HttpTagSelection.open(self._client, [path1, path2])
        uut.delete_tags_from_server()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    def test__server_selection_created__open_tags__existing_selection_edited_on_next_call(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path1}]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = HttpTagSelection.open(self._client, [path1])
        uut.open_tags([path2])
        uut.delete_tags_from_server()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "PUT",
                "/nitag/v2/selections/{id}",
                params={"id": token},
                data={"searchPaths": AnyOrderList([path1, path2]), "id": token},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    def test__server_selection_expired__api_function_called__selection_recreated_and_operation_retried(
        self,
    ):
        path = "tag1"
        token1 = uuid.uuid4()
        token2 = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path}]
        tokens = [token1, token2]
        tag_delete_results = [core.ApiException("404", http_status_code=404), None]

        def mock_request(method, uri, params=None, data=None):
            if uri == "/nitag/v2/selections":
                data = dict(data)
                data.update({"id": tokens.pop(0)})
                return data, MockResponse(method, uri)
            elif uri.endswith("/tags"):
                if method == "DELETE":
                    result = tag_delete_results.pop(0)
                    if isinstance(result, Exception):
                        raise result
                    else:
                        return result, MockResponse(method, uri)
                else:
                    return tags, MockResponse(method, uri)
            elif uri.startswith("/nitag/v2/selections/"):
                assert method == "DELETE"
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        uut = HttpTagSelection.open(self._client, [path])
        uut.delete_tags_from_server()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token1}),
            mock.call(
                "DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token1}
            ),
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call(
                "DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token2}
            ),
        ]

    @pytest.mark.asyncio
    async def test__no_selection_created_by_constructor__async_api_function_called__selection_created(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, AssertionError())
        )

        uut = HttpTagSelection(
            self._client, [tbase.TagData(path1), tbase.TagData(path2)]
        )
        await uut.delete_tags_from_server_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__selection_created_by_constructor__async_api_function_called__selection_reused(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = await HttpTagSelection.open_async(self._client, [path1, path2])
        await uut.delete_tags_from_server_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__server_selection_created__open_tags__existing_selection_edited_on_next_async_call(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path1}]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = await HttpTagSelection.open_async(self._client, [path1])
        uut.open_tags([path2])
        await uut.delete_tags_from_server_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "PUT",
                "/nitag/v2/selections/{id}",
                params={"id": token},
                data={"searchPaths": AnyOrderList([path1, path2]), "id": token},
            ),
            mock.call("DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__server_selection_expired__async_api_function_called__selection_recreated_and_operation_retried(
        self,
    ):
        path = "tag1"
        token1 = uuid.uuid4()
        token2 = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path}]
        tokens = [token1, token2]
        tag_delete_results = [core.ApiException("404", http_status_code=404), None]

        def mock_request(method, uri, params=None, data=None):
            if uri == "/nitag/v2/selections":
                data = dict(data)
                data.update({"id": tokens.pop(0)})
                return data, MockResponse(method, uri)
            elif uri.endswith("/tags"):
                if method == "DELETE":
                    result = tag_delete_results.pop(0)
                    if isinstance(result, Exception):
                        raise result
                    else:
                        return result, MockResponse(method, uri)
                else:
                    return tags, MockResponse(method, uri)
            elif uri.startswith("/nitag/v2/selections/"):
                assert method == "DELETE"
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        uut = await HttpTagSelection.open_async(self._client, [path])
        await uut.delete_tags_from_server_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token1}),
            mock.call(
                "DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token1}
            ),
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call(
                "DELETE", "/nitag/v2/selections/{id}/tags", params={"id": token2}
            ),
        ]

    def test__no_selection_created_by_constructor__refresh_metadata__tags_queried(self):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, [])
        )

        uut = HttpTagSelection(
            self._client, [tbase.TagData(path1), tbase.TagData(path2)]
        )
        uut.refresh_metadata()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    def test__selection_created_by_constructor__refresh_metadata__tags_requeried(self):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = HttpTagSelection.open(self._client, [path1, path2])
        uut.refresh_metadata()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    def test__server_selection_created__open_tags__existing_selection_edited_on_refresh_metadata(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path1}]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = HttpTagSelection.open(self._client, [path1])
        uut.open_tags([path2])
        uut.refresh_metadata()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "PUT",
                "/nitag/v2/selections/{id}",
                params={"id": token},
                data={"searchPaths": AnyOrderList([path1, path2]), "id": token},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    def test__server_selection_expired__refresh_metadata__selection_recreated_and_operation_retried(
        self,
    ):
        path = "tag1"
        token1 = uuid.uuid4()
        token2 = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path}]
        tokens = [token1, token2]
        tag_results = [tags, core.ApiException("404", http_status_code=404), []]

        def mock_request(method, uri, params=None, data=None):
            if uri == "/nitag/v2/selections":
                data = dict(data)
                data.update({"id": tokens.pop(0)})
                return data, MockResponse(method, uri)
            elif uri.endswith("/tags"):
                result = tag_results.pop(0)
                if isinstance(result, Exception):
                    raise result
                else:
                    return result, MockResponse(method, uri)
            elif uri.startswith("/nitag/v2/selections/"):
                assert method == "DELETE"
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        uut = HttpTagSelection.open(self._client, [path])
        uut.refresh_metadata()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token1}),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token1}),
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token2}),
        ]

    @pytest.mark.asyncio
    async def test__no_selection_created_by_constructor__refresh_metadata_async__tags_queried(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, [])
        )

        uut = HttpTagSelection(
            self._client, [tbase.TagData(path1), tbase.TagData(path2)]
        )
        await uut.refresh_metadata_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__selection_created_by_constructor__refresh_metadata_async__tags_requeried(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = await HttpTagSelection.open_async(self._client, [path1, path2])
        await uut.refresh_metadata_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1, path2])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__server_selection_created__open_tags__existing_selection_edited_on_refresh_metadata_async(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        token = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path1}]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = await HttpTagSelection.open_async(self._client, [path1])
        uut.open_tags([path2])
        await uut.refresh_metadata_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path1])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "PUT",
                "/nitag/v2/selections/{id}",
                params={"id": token},
                data={"searchPaths": AnyOrderList([path1, path2]), "id": token},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
        ]

    @pytest.mark.asyncio
    async def test__server_selection_expired__refresh_metadata_async__selection_recreated_and_operation_retried(
        self,
    ):
        path = "tag1"
        token1 = uuid.uuid4()
        token2 = uuid.uuid4()
        tags = [{"type": "DATE_TIME", "path": path}]
        tokens = [token1, token2]
        tag_results = [tags, core.ApiException("404", http_status_code=404), []]

        def mock_request(method, uri, params=None, data=None):
            if uri == "/nitag/v2/selections":
                data = dict(data)
                data.update({"id": tokens.pop(0)})
                return data, MockResponse(method, uri)
            elif uri.endswith("/tags"):
                result = tag_results.pop(0)
                if isinstance(result, Exception):
                    raise result
                else:
                    return result, MockResponse(method, uri)
            elif uri.startswith("/nitag/v2/selections/"):
                assert method == "DELETE"
            else:
                assert False

        self._client.all_requests.configure_mock(side_effect=mock_request)

        uut = await HttpTagSelection.open_async(self._client, [path])
        await uut.refresh_metadata_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token1}),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token1}),
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList([path])},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token2}),
        ]

    def test__refresh_values__values_loaded(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        timestamp = datetime.now(timezone.utc)
        timestamp_str = timestamp.isoformat().rsplit("+", 1)[0] + "Z"
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        values = [
            {"path": path1},
            {
                "path": path2,
                "current": {
                    "value": {"value": "2", "type": "INT"},
                    "timestamp": timestamp_str,
                },
                "aggregates": {"min": "1", "max": "5", "count": 4, "avg": 2.5},
            },
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags, values)
        )

        uut = HttpTagSelection.open(self._client, paths)
        uut.refresh_values()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("GET", "/nitag/v2/selections/{id}/values", params={"id": token}),
        ]

        value = uut.read(path2, include_timestamp=True, include_aggregates=True)
        assert uut.read(path1, include_timestamp=True, include_aggregates=True) is None

        assert self._client.all_requests.call_count == 3
        assert value is not None
        assert 4 == value.count
        assert tbase.DataType.INT32 == value.data_type
        assert 5 == value.max
        assert 2.5 == value.mean
        assert 1 == value.min
        assert path2 == value.path
        assert timestamp == value.timestamp
        assert 2 == value.value

    @pytest.mark.asyncio
    async def test__refresh_values_async__values_loaded(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        timestamp = datetime.now(timezone.utc)
        timestamp_str = timestamp.isoformat().rsplit("+", 1)[0] + "Z"
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        values = [
            {"path": path1},
            {
                "path": path2,
                "current": {
                    "value": {"value": "2", "type": "INT"},
                    "timestamp": timestamp_str,
                },
                "aggregates": {"min": "1", "max": "5", "count": 4, "avg": 2.5},
            },
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags, values)
        )

        uut = await HttpTagSelection.open_async(self._client, [path1, path2])
        await uut.refresh_values_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call("GET", "/nitag/v2/selections/{id}/values", params={"id": token}),
        ]

        value = uut.read(path2, include_timestamp=True, include_aggregates=True)
        assert uut.read(path1, include_timestamp=True, include_aggregates=True) is None

        assert self._client.all_requests.call_count == 3
        assert value is not None
        assert 4 == value.count
        assert tbase.DataType.INT32 == value.data_type
        assert 5 == value.max
        assert 2.5 == value.mean
        assert 1 == value.min
        assert path2 == value.path
        assert timestamp == value.timestamp
        assert 2 == value.value

    def test__refresh__tags_and_values_reloaded(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        timestamp = datetime.now(timezone.utc)
        timestamp_str = timestamp.isoformat().rsplit("+", 1)[0] + "Z"
        token = uuid.uuid4()
        tag1 = {"type": "DATE_TIME", "path": path1}
        tag2 = {"type": "INT", "path": path2}
        tags = [tag1, tag2]
        values = {
            "totalCount": 2,
            "tagsWithValues": [
                # Update the type, to verify that tag data is reloaded
                {"tag": {"path": path1, "type": "STRING"}},
                {
                    "tag": tag2,
                    "current": {
                        "value": {"value": "2", "type": "INT"},
                        "timestamp": timestamp_str,
                    },
                    "aggregates": {"min": "1", "max": "5", "count": 4, "avg": 2.5},
                },
            ],
        }
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags, values)
        )

        uut = HttpTagSelection.open(self._client, [path1, path2])
        uut.refresh()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "GET",
                "/nitag/v2/selections/{id}/tags-with-values",
                params={"id": token},
            ),
        ]

        assert tbase.DataType.STRING == uut.metadata[path1].data_type
        assert tbase.DataType.INT32 == uut.metadata[path2].data_type

        value = uut.read(path2, include_timestamp=True, include_aggregates=True)
        assert uut.read(path1, include_timestamp=True, include_aggregates=True) is None

        assert self._client.all_requests.call_count == 3
        assert value is not None
        assert 4 == value.count
        assert tbase.DataType.INT32 == value.data_type
        assert 5 == value.max
        assert 2.5 == value.mean
        assert 1 == value.min
        assert path2 == value.path
        assert timestamp == value.timestamp
        assert 2 == value.value

    @pytest.mark.asyncio
    async def test__refresh_async__tags_and_values_reloaded(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        timestamp = datetime.now(timezone.utc)
        timestamp_str = timestamp.isoformat().rsplit("+", 1)[0] + "Z"
        token = uuid.uuid4()
        tag1 = {"type": "DATE_TIME", "path": path1}
        tag2 = {"type": "INT", "path": path2}
        tags = [tag1, tag2]
        values = {
            "totalCount": 2,
            "tagsWithValues": [
                # Update the type, to verify that tag data is reloaded
                {"tag": {"path": path1, "type": "STRING"}},
                {
                    "tag": tag2,
                    "current": {
                        "value": {"value": "2", "type": "INT"},
                        "timestamp": timestamp_str,
                    },
                    "aggregates": {"min": "1", "max": "5", "count": 4, "avg": 2.5},
                },
            ],
        }
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags, values)
        )

        uut = await HttpTagSelection.open_async(self._client, [path1, path2])
        await uut.refresh_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "GET",
                "/nitag/v2/selections/{id}/tags-with-values",
                params={"id": token},
            ),
        ]

        assert tbase.DataType.STRING == uut.metadata[path1].data_type
        assert tbase.DataType.INT32 == uut.metadata[path2].data_type

        value = uut.read(path2, include_timestamp=True, include_aggregates=True)
        assert uut.read(path1, include_timestamp=True, include_aggregates=True) is None

        assert self._client.all_requests.call_count == 3
        assert value is not None
        assert 4 == value.count
        assert tbase.DataType.INT32 == value.data_type
        assert 5 == value.max
        assert 2.5 == value.mean
        assert 1 == value.min
        assert path2 == value.path
        assert timestamp == value.timestamp
        assert 2 == value.value

    def test__reset_aggregates__aggregates_reset_on_server(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = HttpTagSelection.open(self._client, paths)
        uut.reset_aggregates()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "POST",
                "/nitag/v2/selections/{id}/reset-aggregates",
                params={"id": token},
                data=None,
            ),
        ]

    @pytest.mark.asyncio
    async def test__reset_aggregates_async__aggregates_reset_on_server(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        token = uuid.uuid4()
        tags = [
            {"type": "DATE_TIME", "path": path1},
            {"type": "INT", "path": path2},
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, tags)
        )

        uut = await HttpTagSelection.open_async(self._client, paths)
        await uut.reset_aggregates_async()

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/selections",
                params=None,
                data={"searchPaths": AnyOrderList(paths)},
            ),
            mock.call("GET", "/nitag/v2/selections/{id}/tags", params={"id": token}),
            mock.call(
                "POST",
                "/nitag/v2/selections/{id}/reset-aggregates",
                params={"id": token},
                data=None,
            ),
        ]
