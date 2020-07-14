from datetime import datetime, timedelta

import pytest  # type: ignore
from systemlink.clients import tag as tbase
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer
from systemlink.clients.tag._core._system_time_stamper import SystemTimeStamper
from systemlink.clients.tag._http._http_buffered_tag_writer import HttpBufferedTagWriter

from .httpclienttestbase import HttpClientTestBase


class TestHttpBufferedTagWriter(HttpClientTestBase):
    def setup_method(self, method):
        super().setup_method(method)

        self._uut = HttpBufferedTagWriter(
            self._client, SystemTimeStamper(), 10, ManualResetTimer.null_timer
        )

    def test__write_buffered__send_buffered_writes__sends_write(self):
        path = "tag"
        value = 2
        timestamp = datetime.now()

        self._uut.write(path, tbase.DataType.INT32, value, timestamp=timestamp)
        self._uut.send_buffered_writes()

        assert self._client.all_requests.call_count == 1
        call = self._client.all_requests.call_args_list[0]
        assert ("POST", "/nitag/v2/update-current-values",) == call[0]
        data = call[1].get("data")
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0].get("path") == path
        updates = data[0].get("updates")
        assert isinstance(updates, list)
        utctime = datetime.utcfromtimestamp(timestamp.timestamp()).isoformat() + "Z"
        assert updates == [
            {"value": {"type": "INT", "value": str(value)}, "timestamp": utctime}
        ]

    @pytest.mark.asyncio
    async def test__write_buffered__send_buffered_writes_async__sends_write(self):
        path = "tag"
        value = 2
        timestamp = datetime.now()

        await self._uut.write_async(
            path, tbase.DataType.INT32, value, timestamp=timestamp
        )
        await self._uut.send_buffered_writes_async()

        assert self._client.all_requests.call_count == 1
        call = self._client.all_requests.call_args_list[0]
        assert ("POST", "/nitag/v2/update-current-values",) == call[0]
        data = call[1].get("data")
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0].get("path") == path
        updates = data[0].get("updates")
        assert isinstance(updates, list)
        utctime = datetime.utcfromtimestamp(timestamp.timestamp()).isoformat() + "Z"
        assert updates == [
            {"value": {"type": "INT", "value": str(value)}, "timestamp": utctime}
        ]

    def test__multiple_writes_buffered_for_same_tag__send_buffered_writes__writes_combined_into_one_batch(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        value1 = 2
        value2 = 5
        value3 = 9
        timestamp1 = datetime.now()
        timestamp2 = timestamp1 + timedelta(seconds=1)
        timestamp3 = timestamp1 + timedelta(seconds=2)

        self._uut.write(path1, tbase.DataType.INT32, value1, timestamp=timestamp1)
        self._uut.write(path2, tbase.DataType.UINT64, value2, timestamp=timestamp2)
        self._uut.write(path1, tbase.DataType.INT32, value3, timestamp=timestamp3)
        self._uut.send_buffered_writes()

        assert self._client.all_requests.call_count == 1
        call = self._client.all_requests.call_args_list[0]
        assert ("POST", "/nitag/v2/update-current-values",) == call[0]
        data = call[1]["data"]
        assert len(data) == 2
        assert data[0]["path"] == path1
        assert data[1]["path"] == path2
        utctime1 = datetime.utcfromtimestamp(timestamp1.timestamp()).isoformat() + "Z"
        utctime2 = datetime.utcfromtimestamp(timestamp2.timestamp()).isoformat() + "Z"
        utctime3 = datetime.utcfromtimestamp(timestamp3.timestamp()).isoformat() + "Z"
        assert data[0]["updates"] == [
            {"value": {"type": "INT", "value": str(value1)}, "timestamp": utctime1},
            {"value": {"type": "INT", "value": str(value3)}, "timestamp": utctime3},
        ]
        assert data[1]["updates"] == [
            {"value": {"type": "U_INT64", "value": str(value2)}, "timestamp": utctime2}
        ]

    def test__write_buffered__clear_buffered_writes__buffer_is_emptied(self):
        path = "tag"
        value = 2
        timestamp = datetime.now()

        self._uut.write(
            "Not path",
            tbase.DataType.DOUBLE,
            12,
            timestamp=timestamp + timedelta(seconds=1),
        )
        self._uut.clear_buffered_writes()
        self._uut.write(path, tbase.DataType.INT32, value, timestamp=timestamp)
        self._uut.send_buffered_writes()

        assert self._client.all_requests.call_count == 1
        call = self._client.all_requests.call_args_list[0]
        assert ("POST", "/nitag/v2/update-current-values",) == call[0]
        data = call[1]["data"]
        assert data[0]["path"] == path
        utctime = datetime.utcfromtimestamp(timestamp.timestamp()).isoformat() + "Z"
        assert data[0]["updates"] == [
            {"value": {"type": "INT", "value": str(value)}, "timestamp": utctime}
        ]

    def test__writes_buffered__send_buffered_writes__buffer_is_emptied(self):
        path = "tag1"
        value1 = 2
        value2 = 5
        timestamp1 = datetime.now()
        timestamp2 = timestamp1 + timedelta(seconds=1)
        self._uut.write(path, tbase.DataType.INT32, value1, timestamp=timestamp1)

        self._uut.send_buffered_writes()
        self._uut.write(path, tbase.DataType.INT32, value2, timestamp=timestamp2)
        self._uut.send_buffered_writes()

        assert self._client.all_requests.call_count == 2
        call1, call2 = self._client.all_requests.call_args_list
        assert ("POST", "/nitag/v2/update-current-values",) == call1[0]
        assert ("POST", "/nitag/v2/update-current-values",) == call2[0]
        data1 = call1[1]["data"]
        data2 = call2[1]["data"]
        assert data1[0]["path"] == path
        assert data2[0]["path"] == path
        utctime1 = datetime.utcfromtimestamp(timestamp1.timestamp()).isoformat() + "Z"
        utctime2 = datetime.utcfromtimestamp(timestamp2.timestamp()).isoformat() + "Z"
        assert data1[0]["updates"] == [
            {"value": {"type": "INT", "value": str(value1)}, "timestamp": utctime1}
        ]
        assert data2[0]["updates"] == [
            {"value": {"type": "INT", "value": str(value2)}, "timestamp": utctime2}
        ]
