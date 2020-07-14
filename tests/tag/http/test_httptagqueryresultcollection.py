from unittest import mock

import pytest  # type: ignore
from systemlink.clients import core, tag as tbase
from systemlink.clients.tag._http._http_tag_query_result_collection import (
    HttpTagQueryResultCollection,
)

from .httpclienttestbase import HttpClientTestBase


class TestHttpTagQueryResultCollection(HttpClientTestBase):
    def test__constructed__first_page_includes_data_from_query(self):
        path1 = "tag1"
        path2 = "tag2"
        total_count = 3
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
        response = {
            "totalCount": total_count,
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

        uut = HttpTagQueryResultCollection(
            self._client, None, None, None, 0, 2, response, None
        )
        page = next(iter(uut))
        assert total_count == uut.total_count
        assert 2 == len(page)
        assert path1 == page[0].path
        assert tbase.DataType.BOOLEAN == page[0].data_type
        assert page[0].collect_aggregates is True
        assert keywords == sorted(page[0].keywords)
        assert sorted(public_properties.items()) == sorted(page[0].properties.items())
        assert dummy_tag.retention_count == page[0].retention_count
        assert dummy_tag.retention_days == page[0].retention_days
        assert dummy_tag.retention_type == page[0].retention_type

        assert path2 == page[1].path
        assert tbase.DataType.DOUBLE == page[1].data_type
        assert page[1].collect_aggregates is False
        assert 0 == len(page[1].keywords)
        assert 0 == len(page[1].properties)
        assert page[1].retention_count is None
        assert page[1].retention_days is None
        assert tbase.RetentionType.NONE == page[1].retention_type

    def test__constructed_with_invalid_first_page__raises(self):
        mock_request = mock.Mock(method="GET", url="http://localhost")
        mock_response = mock.Mock(request=mock_request)
        with pytest.raises(core.ApiException):
            HttpTagQueryResultCollection(
                self._client, None, None, None, 0, None, {}, mock_response
            )

    def test__constructed_with_empty_first_page__no_error(self):
        total_count = 2
        response = {"totalCount": total_count, "tags": []}
        uut = HttpTagQueryResultCollection(
            self._client, None, None, None, total_count, None, response, None
        )
        assert total_count == uut.total_count
        assert 0 == len(list(uut))

        response = {"totalCount": 0, "tags": []}
        uut = HttpTagQueryResultCollection(
            self._client, None, None, None, 0, None, response, None
        )
        assert 0 == uut.total_count
        assert 0 == len(list(uut))

    def test__provided_with_new_datatype__datatype_value_is_unknown(self):
        response = {
            "totalCount": 1,
            "tags": [{"type": "SOME_NEW_VALUE", "path": "tag"}],
        }
        uut = HttpTagQueryResultCollection(
            self._client, None, None, None, 0, None, response, None
        )
        page = next(iter(uut))
        assert 1 == len(page)
        assert tbase.DataType.UNKNOWN == page[0].data_type

    def test__reset_query__requeries_pages_with_all_params(self):
        paths = "tag1,tag2"
        keywords = "keyword1,keyword2"
        properties = "prop1=value1,prop2=value2"
        take = 8
        response = {"totalCount": 2, "tags": [{"type": "STRING", "path": "tag1"}]}
        uut = HttpTagQueryResultCollection(
            self._client, paths, keywords, properties, 0, take, response, None
        )
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([response] * 2)
        )

        next(iter(uut))  # Drain the cached page
        list(uut)  # Iterate over all pages (from the beginning)

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={
                    "path": paths,
                    "keywords": keywords,
                    "properties": properties,
                    "skip": "0",
                    "take": str(take),
                },
            ),
            mock.call(
                "GET",
                "/nitag/v2/tags",
                params={
                    "path": paths,
                    "keywords": keywords,
                    "properties": properties,
                    "skip": "1",
                    "take": str(take),
                },
            ),
        ]

    def test__move_next_page_async__current_page_has_data_for_second_page(self):
        path1 = "tag1"
        path2 = "tag2"
        total_count = 3
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
        response = {
            "totalCount": total_count,
            "tags": [{"type": "DOUBLE", "path": path1}],
        }

        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                [
                    {
                        "totalCount": total_count,
                        "tags": [
                            {
                                "type": "U_INT64",
                                "properties": all_properties,
                                "path": path2,
                                "keywords": keywords,
                                "collectAggregates": True,
                            }
                        ],
                    }
                ]
            )
        )

        uut = HttpTagQueryResultCollection(
            self._client, None, None, None, 0, 1, response, None
        )
        itr = iter(uut)
        next(itr)
        page = next(itr)  # Retrieve the second page
        assert total_count == uut.total_count
        assert 1 == len(page)
        assert path2 == page[0].path
        assert tbase.DataType.UINT64 == page[0].data_type
        assert page[0].collect_aggregates is True
        assert keywords == sorted(page[0].keywords)
        assert sorted(public_properties.items()) == sorted(page[0].properties.items())
        assert dummy_tag.retention_count == page[0].retention_count
        assert dummy_tag.retention_days == page[0].retention_days
        assert dummy_tag.retention_type == page[0].retention_type

    def test__total_count_changes__move_next_page_async__total_count_updated(self):
        tags = [{"type": "STRING", "path": "tag1"}]
        response = {"totalCount": 2, "tags": tags}
        uut = HttpTagQueryResultCollection(
            self._client, None, None, None, 0, 1, response, None
        )
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([{"totalCount": 3, "tags": tags}])
        )

        assert 2 == uut.total_count
        itr = iter(uut)
        next(itr)
        next(itr)  # Retrieve the second page
        assert 3 == uut.total_count

    def test__move_next_page_async__page_can_be_empty(self):
        response = {"totalCount": 2, "tags": [{"type": "STRING", "path": "tag1"}]}
        uut = HttpTagQueryResultCollection(
            self._client, None, None, None, 0, 1, response, None
        )
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request([{"totalCount": 1, "tags": []}])
        )

        assert 1 == len(list(uut))
