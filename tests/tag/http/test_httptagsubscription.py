from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from unittest import mock

import events
import pytest  # type: ignore
from systemlink.clients import core, tag as tbase
from systemlink.clients.core._internal._timestamp_utilities import TimestampUtilities
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer
from systemlink.clients.tag._http._http_tag_subscription import HttpTagSubscription

from .httpclienttestbase import HttpClientTestBase, MockResponse


class TestHttpTagSubscription(HttpClientTestBase):
    @classmethod
    def _get_mock_request(cls, token, query_result, heartbeat_result=None):
        # Override the parent class's implementation with a more specific one

        def mock_request(method, uri, params=None, data=None):
            if (method, uri) == ("POST", "/nitag/v2/subscriptions"):
                return {"subscriptionId": token}, MockResponse(method, uri)
            elif method == "GET":
                return query_result, MockResponse(method, uri)
            elif method == "DELETE":
                return None, MockResponse(method, uri)
            elif method == "PUT" and uri.endswith("/heartbeat"):
                if isinstance(heartbeat_result, Exception):
                    raise heartbeat_result
                else:
                    return heartbeat_result, MockResponse(method, uri)
            assert False

        return mock_request

    def test__create__subscription_created_on_server(self):
        token = "id"
        paths = ["tag1", "tag2", "tag3"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        HttpTagSubscription.create(
            self._client,
            paths,
            ManualResetTimer.null_timer,
            ManualResetTimer.null_timer,
        )

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/subscriptions",
                params=None,
                data={"tags": paths, "updatesOnly": True},
            ),
            mock.call(
                "GET",
                "/nitag/v2/subscriptions/{id}/values/current",
                params={"id": token},
            ),
        ]

    @pytest.mark.asyncio
    async def test__create_async__subscription_created_on_server(self):
        token = "id"
        paths = ["tag1", "tag2", "tag3"]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        await HttpTagSubscription.create_async(
            self._client,
            paths,
            ManualResetTimer.null_timer,
            ManualResetTimer.null_timer,
        )

        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/subscriptions",
                params=None,
                data={"tags": paths, "updatesOnly": True},
            ),
            mock.call(
                "GET",
                "/nitag/v2/subscriptions/{id}/values/current",
                params={"id": token},
            ),
        ]

    def test__update_timer_elapses__server_queried_for_updates_and_timer_reset(self):
        token = "test subscription"
        paths = []
        timer = mock.Mock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        uut = HttpTagSubscription.create(
            self._client, paths, timer, ManualResetTimer.null_timer
        )

        assert uut
        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/subscriptions",
                params=None,
                data={"tags": paths, "updatesOnly": True},
            ),
            mock.call(
                "GET",
                "/nitag/v2/subscriptions/{id}/values/current",
                params={"id": token},
            ),
        ]
        timer.start.assert_called_once_with()

        timer.elapsed()

        assert self._client.all_requests.call_count == 3
        self._client.all_requests.assert_called_with(
            "GET", "/nitag/v2/subscriptions/{id}/values/current", params={"id": token},
        )
        assert timer.start.call_count == 2
        assert len(timer.method_calls) == 2

    def test__tags_updates_received_from_server__tag_changed_event_fired_with_each_update(
        self,
    ):
        token = "test subscription"
        timestamp = datetime.now(timezone.utc)
        timestamp_str = TimestampUtilities.datetime_to_str(timestamp)
        timer = mock.Mock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        updates_list = self._one_update_of_each_type(timestamp_str)
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                token,
                {
                    "subscriptionUpdates": [
                        {"subscriptionId": token, "updates": updates_list}
                    ]
                },
            )
        )

        updates = (
            {}
        )  # type: Dict[str, Tuple[tbase.TagData, Optional[tbase.TagValueReader]]]
        uut = HttpTagSubscription.create(
            self._client, [], timer, ManualResetTimer.null_timer
        )

        def on_tag_changed(
            tag: tbase.TagData, reader: Optional[tbase.TagValueReader]
        ) -> None:
            assert tag is not None
            assert tag.path
            assert tag.path not in updates
            updates[tag.path] = (tag, reader)

        uut.tag_changed += on_tag_changed

        timer.elapsed()

        value_converters = {
            "DOUBLE": float,
            "INT": int,
            "STRING": str,
            "BOOLEAN": {"True": True, "False": False}.get,
            "U_INT64": int,
            "DATE_TIME": TimestampUtilities.str_to_datetime,
        }

        def check_args(
            data: Dict[str, Any],
            tag: tbase.TagData,
            reader: Optional[tbase.TagValueReader],
        ) -> None:
            assert tbase.DataType.from_api_name(data["type"]) == tag.data_type
            convert_value = value_converters[data["type"]]
            assert reader is not None
            value = reader.read(include_timestamp=True, include_aggregates=True)
            assert value is not None
            assert convert_value(data["value"]) == value.value
            assert timestamp == value.timestamp
            if "aggregates" not in data:
                assert value.count is None
            else:
                assert value.count is not None
                assert data["aggregates"]["count"] == value.count
                if "avg" in data["aggregates"]:
                    assert data["aggregates"]["avg"] == value.mean
                    assert convert_value(data["aggregates"]["min"]) == value.min
                    assert convert_value(data["aggregates"]["max"]) == value.max

        assert 6 == len(updates)
        for u in updates_list:
            path = u["tag"]["path"]
            assert path in updates
            check_args(u, *updates[path])

    def test__updates_received_on_create__tag_changed_event_doesnt_see_those_updates(
        self,
    ):
        token = "test subscription"
        timestamp = datetime.now(timezone.utc)
        timestamp_str = TimestampUtilities.datetime_to_str(timestamp)
        timer = mock.Mock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        updates_list = self._one_update_of_each_type(timestamp_str)
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                token,
                {
                    "subscriptionUpdates": [
                        {"subscriptionId": token, "updates": updates_list}
                    ]
                },
            )
        )

        uut = HttpTagSubscription.create(
            self._client, [], timer, ManualResetTimer.null_timer
        )

        assert self._client.all_requests.call_count == 2

        def on_tag_changed(
            tag: tbase.TagData, reader: Optional[tbase.TagValueReader]
        ) -> None:
            assert False, "Should not have received any updates"

        uut.tag_changed += on_tag_changed
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(None, {})
        )

        timer.elapsed()

        assert self._client.all_requests.call_count == 3
        self._client.all_requests.assert_called_with(
            "GET", "/nitag/v2/subscriptions/{id}/values/current", params={"id": token},
        )

    def test__update_fails__update_timer_elapsed__error_ignored(self):
        token = "test subscription"
        timer = mock.Mock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )
        updates = []

        def on_tag_changed(
            tag: tbase.TagData, reader: Optional[tbase.TagValueReader]
        ) -> None:
            updates.append((tag, reader))

        uut = HttpTagSubscription.create(
            self._client, [], timer, ManualResetTimer.null_timer
        )
        uut.tag_changed += on_tag_changed

        assert timer.start.call_count == 1
        assert self._client.all_requests.call_count == 2
        assert self._client.all_requests.call_args[0][1].endswith("/values/current")

        self._client.all_requests.configure_mock(side_effect=core.ApiException("oops"))

        timer.elapsed()
        assert timer.start.call_count == 2
        assert self._client.all_requests.call_count == 3
        assert self._client.all_requests.call_args[0][1].endswith("/values/current")

        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(None, {})
        )

        timer.elapsed()
        assert timer.start.call_count == 3
        assert self._client.all_requests.call_count == 4
        assert self._client.all_requests.call_args[0][1].endswith("/values/current")

        assert 0 == len(updates)

    def test__invalid_subscription_updates_received__those_updates_skipped(self):
        token = "test subscription"
        timestamp = datetime.now(timezone.utc)
        timestamp_str = TimestampUtilities.datetime_to_str(timestamp)
        timer = mock.Mock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        good_update = self._one_update_of_each_type(timestamp_str)[0]
        updates_list = [
            None,
            {},
            {"value": "invalid"},
            {"value": "invalid", "type": "STRING"},
            {
                "value": "invalid",
                "type": "STRING",
                "tag": {"type": "STRING", "path": "invalid"},
            },
            {
                "value": "invalid",
                "type": "STRING",
                "timestamp": None,
                "tag": {"type": "STRING", "path": "invalid"},
            },
            {"value": "invalid", "type": "STRING", "timestamp": timestamp_str},
            {
                "value": "invalid",
                "type": "STRING",
                "timestamp": timestamp_str,
                "tag": {"type": "STRING", "path": ""},
            },
            {
                "value": "invalid",
                "type": "BOOLEAN",
                "timestamp": timestamp_str,
                "tag": {"type": "BOOLEAN", "path": "bool"},
            },
            good_update,
        ]
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                token,
                {
                    "subscriptionUpdates": [
                        None,
                        {},
                        {"updates": []},
                        {"subscriptionId": token, "updates": updates_list},
                    ],
                },
            )
        )

        def on_tag_changed(
            tag: tbase.TagData, value: Optional[tbase.TagValueReader]
        ) -> None:
            assert tag is not None
            assert tag.path
            assert tag.path not in updates
            updates[tag.path] = (tag, value)

        updates = (
            {}
        )  # type: Dict[str, Tuple[tbase.TagData, Optional[tbase.TagValueReader]]]
        uut = HttpTagSubscription.create(
            self._client, [], timer, ManualResetTimer.null_timer
        )
        uut.tag_changed += on_tag_changed

        timer.elapsed()

        assert 2 == len(updates)
        assert "bool" in updates
        (tag, reader) = updates["bool"]
        assert tbase.DataType.BOOLEAN == tag.data_type
        with pytest.raises(core.ApiException):
            reader.read()

        assert "double" in updates
        (tag, reader) = updates["double"]
        assert tbase.DataType.DOUBLE == tag.data_type
        value = reader.read(include_timestamp=True, include_aggregates=True)
        assert 3.14 == value.value
        assert timestamp == value.timestamp
        assert value.count is not None
        assert 1.1 == value.min
        assert 4.4 == value.max
        assert 3 == value.count
        assert 2.88 == value.mean

    def test__unknown_data_type_received_in_update__tag_changed_event_still_fires(self):
        token = "test subscription"
        timestamp = datetime.now(timezone.utc)
        timestamp_str = TimestampUtilities.datetime_to_str(timestamp)
        timer = mock.Mock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                token,
                {
                    "subscriptionUpdates": [
                        {
                            "subscriptionId": token,
                            "updates": [
                                {
                                    "value": "unknown",
                                    "type": "BLAH",
                                    "timestamp": timestamp_str,
                                    "tag": {"type": "BLAH", "path": "unknown"},
                                    "aggregates": {
                                        "min": "1.1",
                                        "max": "4.4",
                                        "count": 3,
                                        "avg": 2.88,
                                    },
                                }
                            ],
                        },
                    ],
                },
            )
        )

        def on_tag_changed(
            tag: tbase.TagData, reader: Optional[tbase.TagValueReader]
        ) -> None:
            assert tag is not None
            assert tag.path
            assert tag.path not in updates
            updates[tag.path] = (tag, reader)

        updates = (
            {}
        )  # type: Dict[str, Tuple[tbase.TagData, Optional[tbase.TagValueReader]]]
        uut = HttpTagSubscription.create(
            self._client, [], timer, ManualResetTimer.null_timer
        )
        uut.tag_changed += on_tag_changed

        timer.elapsed()

        assert 1 == len(updates)
        assert "unknown" in updates
        (tag, reader) = updates["unknown"]
        assert tbase.DataType.UNKNOWN == tag.data_type

        assert reader is None

    def test__exit__subscription_deleted_from_server(self):
        token = "test subscription"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        with HttpTagSubscription.create(
            self._client, [], ManualResetTimer.null_timer, ManualResetTimer.null_timer
        ):
            pass

        assert self._client.all_requests.call_args == mock.call(
            "DELETE", "/nitag/v2/subscriptions/{id}", params={"id": token}
        )

    def test__exit__timer_stopped_and_callback_unregistered(self):
        token = "id"
        timer = mock.MagicMock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        with HttpTagSubscription.create(
            self._client, [], timer, ManualResetTimer.null_timer
        ):
            assert timer.stop.call_count == 0
            assert len(timer.elapsed) == 1

        assert timer.stop.call_count == 1
        assert len(timer.elapsed) == 0

    @pytest.mark.asyncio
    async def test__aexit__subscription_deleted_from_server(self):
        token = "test subscription"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        async with await HttpTagSubscription.create_async(
            self._client, [], ManualResetTimer.null_timer, ManualResetTimer.null_timer
        ):
            pass

        assert self._client.all_requests.call_args == mock.call(
            "DELETE", "/nitag/v2/subscriptions/{id}", params={"id": token}
        )

    @pytest.mark.asyncio
    async def test__aexit__timer_stopped_and_callback_unregistered(self):
        token = "test subscription"
        timer = mock.MagicMock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        async with await HttpTagSubscription.create_async(
            self._client, [], timer, ManualResetTimer.null_timer
        ):
            assert timer.stop.call_count == 0
            assert len(timer.elapsed) == 1

        assert timer.stop.call_count == 1
        assert len(timer.elapsed) == 0

    def test__close__subscription_deleted_from_server(self):
        token = "test subscription"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        uut = HttpTagSubscription.create(
            self._client, [], ManualResetTimer.null_timer, ManualResetTimer.null_timer
        )
        uut.close()

        assert self._client.all_requests.call_args == mock.call(
            "DELETE", "/nitag/v2/subscriptions/{id}", params={"id": token}
        )

    def test__close__timer_stopped_and_callback_unregistered(self):
        token = "id"
        timer = mock.MagicMock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        uut = HttpTagSubscription.create(
            self._client, [], timer, ManualResetTimer.null_timer
        )
        assert timer.stop.call_count == 0
        assert len(timer.elapsed) == 1

        uut.close()
        assert timer.stop.call_count == 1
        assert len(timer.elapsed) == 0

    @pytest.mark.asyncio
    async def test__close_async__subscription_deleted_from_server(self):
        token = "test subscription"
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        uut = await HttpTagSubscription.create_async(
            self._client, [], ManualResetTimer.null_timer, ManualResetTimer.null_timer
        )
        await uut.close_async()

        assert self._client.all_requests.call_args == mock.call(
            "DELETE", "/nitag/v2/subscriptions/{id}", params={"id": token}
        )

    @pytest.mark.asyncio
    async def test__close_async__timer_stopped_and_callback_unregistered(self):
        token = "id"
        timer = mock.MagicMock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        uut = await HttpTagSubscription.create_async(
            self._client, [], timer, ManualResetTimer.null_timer
        )
        assert timer.stop.call_count == 0
        assert len(timer.elapsed) == 1

        await uut.close_async()
        assert timer.stop.call_count == 1
        assert len(timer.elapsed) == 0

    def test__heartbeat_timer_elapsed__heartbeat_sent_to_server_and_timer_reset(self):
        token = "test subscription"
        timer = mock.MagicMock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token, {})
        )

        uut = HttpTagSubscription.create(
            self._client, [], ManualResetTimer.null_timer, timer
        )
        assert uut
        assert timer.start.call_count == 1

        timer.elapsed()
        assert self._client.all_requests.call_args == mock.call(
            "PUT",
            "/nitag/v2/subscriptions/{id}/heartbeat",
            params={"id": token},
            data=None,
        )
        assert timer.start.call_count == 2

    def test__heartbeat_query_errors__subscription_recreated(self):
        token1 = "test subscription"
        token2 = "second test subscription"
        paths = ["tag1", "tag2", "tag3"]
        timer = mock.MagicMock(ManualResetTimer, wraps=ManualResetTimer.null_timer)
        type(timer).elapsed = events.events._EventSlot("elapsed")
        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(token1, {})
        )

        uut = HttpTagSubscription.create(
            self._client, paths, ManualResetTimer.null_timer, timer
        )

        assert uut
        assert timer.start.call_count == 1
        assert self._client.all_requests.call_count == 2
        assert self._client.all_requests.call_args_list == [
            mock.call(
                "POST",
                "/nitag/v2/subscriptions",
                params=None,
                data={"tags": paths, "updatesOnly": True},
            ),
            mock.call(
                "GET",
                "/nitag/v2/subscriptions/{id}/values/current",
                params={"id": token1},
            ),
        ]

        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(
                token2, {}, core.ApiException("Unknown subscription")
            )
        )

        timer.elapsed()

        assert timer.start.call_count == 2
        assert self._client.all_requests.call_count == 5
        assert self._client.all_requests.call_args_list[-3:] == [
            mock.call(
                "PUT",
                "/nitag/v2/subscriptions/{id}/heartbeat",
                params={"id": token1},
                data=None,
            ),
            mock.call(
                "POST",
                "/nitag/v2/subscriptions",
                params=None,
                data={"tags": paths, "updatesOnly": True},
            ),
            mock.call(
                "GET",
                "/nitag/v2/subscriptions/{id}/values/current",
                params={"id": token2},
            ),
        ]

        self._client.all_requests.configure_mock(
            side_effect=self._get_mock_request(None, None)
        )

        timer.elapsed()

        assert timer.start.call_count == 3
        assert self._client.all_requests.call_count == 6
        assert self._client.all_requests.call_args_list[-1:] == [
            mock.call(
                "PUT",
                "/nitag/v2/subscriptions/{id}/heartbeat",
                params={"id": token2},
                data=None,
            ),
        ]

    @classmethod
    def _one_update_of_each_type(cls, timestamp_str: str) -> List[Any]:
        return [
            {
                "value": "3.14",
                "type": "DOUBLE",
                "timestamp": timestamp_str,
                "tag": {"type": "DOUBLE", "path": "double"},
                "aggregates": {"min": "1.1", "max": "4.4", "count": 3, "avg": 2.88},
            },
            {
                "value": "-2",
                "type": "INT",
                "timestamp": timestamp_str,
                "tag": {"type": "INT", "path": "int"},
                "aggregates": {"min": "-5", "max": "3", "count": 4, "avg": 3.23},
            },
            {
                "value": "testing",
                "type": "STRING",
                "timestamp": timestamp_str,
                "tag": {"type": "STRING", "path": "string"},
                "aggregates": {"count": 3},
            },
            {
                "value": "True",
                "type": "BOOLEAN",
                "timestamp": timestamp_str,
                "tag": {"type": "BOOLEAN", "path": "bool"},
            },
            {
                "value": "103",
                "type": "U_INT64",
                "timestamp": timestamp_str,
                "tag": {"type": "U_INT64", "path": "uint64"},
            },
            {
                "value": timestamp_str,
                "type": "DATE_TIME",
                "timestamp": timestamp_str,
                "tag": {"type": "DATE_TIME", "path": "date"},
            },
        ]
