import datetime
from unittest import mock
from unittest.mock import Mock, PropertyMock

import pytest  # type: ignore
import systemlink.clients.core as core
import systemlink.clients.tag as tbase
from systemlink.clients.tag._core._itime_stamper import ITimeStamper
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer
from systemlink.clients.tag._core._system_time_stamper import SystemTimeStamper

from .mock_manualresettimer import MockManualResetTimer


class TestBufferedTagWriter:
    serialized_timestamp = "2018-11-15T03:47:36.000000+0000"
    timestamp = datetime.datetime.strptime(
        serialized_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z"
    )

    def test__invalid_path__write__raises(self):
        writer = self.MockBufferedTagWriter(None, 1)

        with pytest.raises(ValueError) as excinfo:
            writer.write(None, tbase.DataType.BOOLEAN, False, timestamp=None)
        assert "path " in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            writer.write("", tbase.DataType.BOOLEAN, False, timestamp=None)
        assert "path " in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            writer.write("*", tbase.DataType.BOOLEAN, False, timestamp=None)
        assert "path " in str(excinfo.value)

    def test__invalid_data_type__write__raises(self):
        writer = self.MockBufferedTagWriter(None, 1)
        with pytest.raises(ValueError) as excinfo:
            writer.write("tag", tbase.DataType.UNKNOWN, "test", timestamp=None)
        assert "type " in str(excinfo.value)

    def test__write__item_created_and_buffered(self):
        writer = self.MockBufferedTagWriter(None, 2)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None, return_value=None)

        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        writer.mock_create_item.assert_called_once_with(
            "tag", tbase.DataType.BOOLEAN, "False", self.timestamp
        )
        writer.mock_buffer_value.assert_called_once_with("tag", item)

    def test__null_timestamp_and_no_time_stamper__write__default_time_stamper_used(
        self,
    ):
        writer = self.MockBufferedTagWriter(None, 2)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)

        before_write = datetime.datetime.now(datetime.timezone.utc)
        tolerance_seconds = 0.1

        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        assert writer.mock_create_item.call_count == 1
        assert writer.mock_create_item.call_args[0][:-1] == (
            "tag",
            tbase.DataType.BOOLEAN,
            "False",
        )
        timestamp = writer.mock_create_item.call_args[0][-1]
        assert timestamp is not None
        assert (timestamp - before_write).total_seconds() < tolerance_seconds
        writer.mock_buffer_value.assert_called_once_with("tag", item)

    def test__null_timestamp_and_time_stamper_given__write__time_stamper_used(self):
        date_string = "2019-07-08T18:52:58.230069+0000"
        date_offset = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
        writer = self.MockBufferedTagWriter(Mock(ITimeStamper), 2)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None, return_value=None)
        timestamp_property = PropertyMock(return_value=date_offset)
        type(writer.time_stamper).timestamp = timestamp_property

        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        writer.mock_create_item.assert_called_once_with(
            "tag", tbase.DataType.BOOLEAN, "False", date_offset
        )
        writer.mock_buffer_value.assert_called_once_with("tag", item)
        timestamp_property.assert_called_once_with()

    def test__write__new_timestamp_queried_for_each_value(self):
        writer = self.MockBufferedTagWriter(Mock(ITimeStamper), 3)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        timestamp_property = PropertyMock(
            return_value=datetime.datetime.now(datetime.timezone.utc)
        )
        type(writer.time_stamper).timestamp = timestamp_property

        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        timestamp_property.assert_called_once_with()

        timestamp_property.reset_mock()
        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        timestamp_property.assert_called_once_with()

    def test__buffer_size__write__updates_sent_when_buffer_fills(self):
        writer = self.MockBufferedTagWriter(None, 2)
        item1 = object()
        item2 = object()
        buffer = [item1, item2]

        writer.mock_create_item.configure_mock(side_effect=[item1, item2])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes.configure_mock(side_effect=None)

        assert writer._num_buffered == 0
        assert writer._buffer_limit == 2
        writer.write("tag1", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        writer.mock_copy_buffer.assert_not_called()
        writer.mock_send_writes.assert_not_called()
        assert writer._num_buffered == 1
        writer.write("tag2", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)

        assert writer.mock_create_item.call_args_list == [
            mock.call("tag1", tbase.DataType.BOOLEAN, "False", self.timestamp),
            mock.call("tag2", tbase.DataType.DOUBLE, "1.1", self.timestamp),
        ]
        assert writer.mock_buffer_value.call_args_list == [
            mock.call("tag1", item1),
            mock.call("tag2", item2),
        ]
        writer.mock_copy_buffer.assert_called_once_with()
        writer.mock_send_writes.assert_called_once_with(buffer)

    def test__timer_enabled__write__timer_started(self):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())
        item = object()

        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property
        writer.timer.start.configure_mock(side_effect=None)

        writer.write("tag", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        writer.timer.start.assert_called_once_with()

    def test__timed_flush_errored__write__item_buffered_and_cached_error_raised(self):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())
        item1 = object()
        item2 = object()
        item3 = object()
        buffer = [item1]

        writer.mock_create_item.configure_mock(side_effect=[item1, item2, item3])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes.configure_mock(side_effect=core.ApiException)
        writer.mock_clear_buffer.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property

        writer.write("tag1", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        # Here's where the error is raised by the API
        writer.trigger_flush_event()
        # But here's where the user gets a chance to see the error
        with pytest.raises(core.ApiException):
            writer.write("tag2", tbase.DataType.INT32, -1, timestamp=self.timestamp)
        writer.clear_buffered_writes()  # "Clear" the buffer, or next write would fill it
        writer.write("tag3", tbase.DataType.STRING, "test3", timestamp=self.timestamp)

        writer.mock_send_writes.assert_called_once_with(buffer)
        assert writer.mock_buffer_value.call_args_list == [
            mock.call("tag1", item1),
            mock.call(
                "tag2", item2
            ),  # tag2 should have been buffered despite the error
            mock.call("tag3", item3),
        ]

    def test__create_item_errors__write__user_sees_error(self):
        writer = self.MockBufferedTagWriter(None, 2)
        writer.mock_create_item.configure_mock(side_effect=[ValueError, object()])

        with pytest.raises(ValueError):
            writer.write("tag1", tbase.DataType.UINT64, 1, timestamp=self.timestamp)

        # Yet after the error, other writes can happen
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.write("tag2", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        assert writer.mock_buffer_value.call_count == 1

    @pytest.mark.asyncio
    async def test__invalid_path__write_async__raises(self):
        writer = self.MockBufferedTagWriter(None, 1)

        with pytest.raises(ValueError) as excinfo:
            await writer.write_async(
                None, tbase.DataType.BOOLEAN, False, timestamp=None
            )
        assert "path " in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            await writer.write_async("", tbase.DataType.BOOLEAN, False, timestamp=None)
        assert "path " in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            await writer.write_async("*", tbase.DataType.BOOLEAN, False, timestamp=None)
        assert "path " in str(excinfo.value)

    @pytest.mark.asyncio
    async def test__invalid_data_type__write_async__raises(self):
        writer = self.MockBufferedTagWriter(None, 1)
        with pytest.raises(ValueError) as excinfo:
            await writer.write_async(
                "tag", tbase.DataType.UNKNOWN, "test", timestamp=None
            )
        assert "type " in str(excinfo.value)

    @pytest.mark.asyncio
    async def test__write_async__item_created_and_buffered(self):
        writer = self.MockBufferedTagWriter(None, 2)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)

        await writer.write_async(
            "tag", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp
        )
        writer.mock_create_item.assert_called_once_with(
            "tag", tbase.DataType.BOOLEAN, "False", self.timestamp
        )
        writer.mock_buffer_value.assert_called_once_with("tag", item)

    @pytest.mark.asyncio
    async def test__null_timestamp_and_no_time_stamper__write_async__default_time_stamper_used(
        self,
    ):
        writer = self.MockBufferedTagWriter(None, 2)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)

        before_write = datetime.datetime.now(datetime.timezone.utc)
        tolerance_seconds = 0.1

        await writer.write_async("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        assert writer.mock_create_item.call_count == 1
        assert writer.mock_create_item.call_args[0][:-1] == (
            "tag",
            tbase.DataType.BOOLEAN,
            "False",
        )
        timestamp = writer.mock_create_item.call_args[0][-1]
        assert timestamp is not None
        assert (timestamp - before_write).total_seconds() < tolerance_seconds
        writer.mock_buffer_value.assert_called_once_with("tag", item)

    @pytest.mark.asyncio
    async def test__null_timestamp_and_time_stamper_given__write_async__time_stamper_used(
        self,
    ):
        date_string = "2019-07-08T18:52:58.230069+0000"
        date_offset = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
        writer = self.MockBufferedTagWriter(Mock(ITimeStamper), 2)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        timestamp_property = PropertyMock(return_value=date_offset)
        type(writer.time_stamper).timestamp = timestamp_property

        await writer.write_async("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        writer.mock_create_item.assert_called_once_with(
            "tag", tbase.DataType.BOOLEAN, "False", date_offset
        )
        writer.mock_buffer_value.assert_called_once_with("tag", item)
        timestamp_property.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__write_async__new_timestamp_queried_for_each_value(self):
        writer = self.MockBufferedTagWriter(Mock(ITimeStamper), 3)
        item = object()
        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        timestamp_property = PropertyMock(
            return_value=datetime.datetime.now(datetime.timezone.utc)
        )
        type(writer.time_stamper).timestamp = timestamp_property

        await writer.write_async("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        timestamp_property.assert_called_once_with()
        await writer.write_async("tag", tbase.DataType.BOOLEAN, False, timestamp=None)
        assert timestamp_property.call_args_list == [mock.call(), mock.call()]

    @pytest.mark.asyncio
    async def test__buffer_size__write_async__updates_sent_when_buffer_fills(self):
        writer = self.MockBufferedTagWriter(None, 2)
        item1 = object()
        item2 = object()
        buffer = [item1, item2]

        writer.mock_create_item.configure_mock(side_effect=[item1, item2])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes_async.configure_mock(side_effect=None)

        assert writer._num_buffered == 0
        assert writer._buffer_limit == 2
        await writer.write_async(
            "tag1", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp
        )
        writer.mock_copy_buffer.assert_not_called()
        writer.mock_send_writes_async.assert_not_called()
        assert writer._num_buffered == 1
        await writer.write_async(
            "tag2", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp
        )

        assert writer.mock_create_item.call_args_list == [
            mock.call("tag1", tbase.DataType.BOOLEAN, "False", self.timestamp),
            mock.call("tag2", tbase.DataType.DOUBLE, "1.1", self.timestamp),
        ]
        assert writer.mock_buffer_value.call_args_list == [
            mock.call("tag1", item1),
            mock.call("tag2", item2),
        ]
        writer.mock_copy_buffer.assert_called_once_with()
        writer.mock_send_writes_async.assert_called_once_with(buffer)

    @pytest.mark.asyncio
    async def test__timer_enabled__write_async__timer_started(self):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())
        item = object()

        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property
        writer.timer.start.configure_mock(side_effect=None)

        await writer.write_async(
            "tag", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp
        )
        writer.timer.start.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__timed_flush_errored__write_async__item_buffered_and_cached_error_raised(
        self,
    ):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())
        item1 = object()
        item2 = object()
        item3 = object()
        buffer = [item1]

        writer.mock_create_item.configure_mock(side_effect=[item1, item2, item3])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes.configure_mock(side_effect=core.ApiException)
        writer.mock_clear_buffer.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property

        writer.write("tag1", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        # Here's where the error is raised by the API
        writer.trigger_flush_event()
        # But here's where the user gets a chance to see the error
        with pytest.raises(core.ApiException):
            await writer.write_async(
                "tag2", tbase.DataType.INT32, -1, timestamp=self.timestamp
            )
        writer.clear_buffered_writes()  # "Clear" the buffer, or next write would fill it
        await writer.write_async(
            "tag3", tbase.DataType.STRING, "test3", timestamp=self.timestamp
        )

        writer.mock_send_writes.assert_called_once_with(buffer)
        assert writer.mock_buffer_value.call_args_list == [
            mock.call("tag1", item1),
            mock.call(
                "tag2", item2
            ),  # tag2 should have been buffered despite the error
            mock.call("tag3", item3),
        ]

    def test__items_buffered__clear_buffered_writes__clear_buffer_called(self):
        writer = self.MockBufferedTagWriter(None, 2)
        item1 = object()
        item2 = object()

        writer.mock_create_item.configure_mock(side_effect=[item1, item2])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_clear_buffer.configure_mock(side_effect=None)

        writer.write("tag1", tbase.DataType.STRING, "test1", timestamp=self.timestamp)
        writer.clear_buffered_writes()
        writer.write("tag2", tbase.DataType.UINT64, 1, timestamp=self.timestamp)

        assert writer.mock_buffer_value.call_args_list == [
            mock.call("tag1", item1),
            mock.call("tag2", item2),
        ]
        writer.mock_clear_buffer.assert_called_once_with()

    def test__items_buffered__clear_buffered_writes__flush_timer_stopped(self):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())

        writer.mock_create_item.configure_mock(side_effect=None, return_value=object())
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_clear_buffer.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property

        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        writer.clear_buffered_writes()

        writer.timer.start.assert_called_once_with()
        writer.timer.stop.assert_called_once_with()

    def test__items_buffered__send_buffered_writes__buffer_copied_and_sent(self):
        writer = self.MockBufferedTagWriter(None, 3)
        item1 = object()
        item2 = object()
        buffer = [item1, item2]

        writer.mock_create_item.configure_mock(side_effect=[item1, item2])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes.configure_mock(side_effect=None)

        writer.write("tag1", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        writer.write("tag2", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        writer.send_buffered_writes()

        writer.mock_send_writes.assert_called_once_with(buffer)

    def test__no_items_buffered__send_buffered_writes__nothing_called(self):
        writer = self.MockBufferedTagWriter(None, 2)
        writer.send_buffered_writes()
        # The strict mock will assert no methods were called.

    def test__items_buffered__send_buffered_writes__flush_timer_stopped(self):
        writer = self.MockBufferedTagWriter(None, 3, MockManualResetTimer())
        item = object()
        buffer = [item]

        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property

        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        writer.send_buffered_writes()

        writer.timer.start.assert_called_once_with()
        writer.timer.stop.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__items_buffered__send_buffered_writes_async__buffer_copied_and_sent(
        self,
    ):
        writer = self.MockBufferedTagWriter(None, 3)
        item1 = object()
        item2 = object()
        buffer = [item1, item2]

        writer.mock_create_item.configure_mock(side_effect=[item1, item2])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes_async.configure_mock(side_effect=None)

        writer.write("tag1", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        writer.write("tag2", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        await writer.send_buffered_writes_async()

        writer.mock_send_writes_async.assert_called_once_with(buffer)

    @pytest.mark.asyncio
    async def test__no_items_buffered__send_buffered_writes_async__nothing_called(self):
        writer = self.MockBufferedTagWriter(None, 2)
        await writer.send_buffered_writes_async()
        # The strict mock will assert no methods were called.

    @pytest.mark.asyncio
    async def test__items_buffered__send_buffered_writes_async__flush_timer_stopped(
        self,
    ):
        writer = self.MockBufferedTagWriter(None, 3, MockManualResetTimer())
        item = object()
        buffer = [item]

        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes_async.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property

        writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        await writer.send_buffered_writes_async()

        writer.timer.start.assert_called_once_with()
        writer.timer.stop.assert_called_once_with()

    def test__items_buffered__flush_timer_elapsed__items_sent(self):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())
        item = object()
        buffer = [item]

        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property

        writer.write("tag", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        writer.trigger_flush_event()

        writer.mock_send_writes.assert_called_once_with(buffer)

    def test__send_buffered_writes_already_called__original_flush_timer_elapsed__updates_not_sent(
        self,
    ):
        writer = self.MockBufferedTagWriter(
            SystemTimeStamper(), 2, MockManualResetTimer()
        )
        item1 = object()
        item2 = object()
        buffer = [item1]

        writer.mock_create_item.configure_mock(side_effect=[item1, item2])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_copy_buffer.configure_mock(side_effect=None, return_value=buffer)
        writer.mock_send_writes.configure_mock(side_effect=None)

        writer.write("tag1", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        elapsed_handlers = list(writer.timer.elapsed)
        writer.send_buffered_writes()
        writer.write("tag2", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)

        # Simulate queuing the timer event in parallel to SendBufferedWrites
        # by raising the event using the handlers that were there earlier.
        # (The second write should have replaced them with *new* event handlers. It
        # should also stop the original timer, but if the timer is already elapsing, it
        # should be ignored.)
        assert elapsed_handlers is not None
        for h in elapsed_handlers:
            h()

        writer.mock_copy_buffer.assert_called_once_with()
        writer.mock_send_writes.assert_called_once_with(buffer)

    def test__clear_buffered_writes_already_called__original_flush_timer_elapsed__writes_not_sent(
        self,
    ):
        writer = self.MockBufferedTagWriter(
            SystemTimeStamper(), 2, MockManualResetTimer()
        )
        item1 = object()
        item2 = object()

        writer.mock_create_item.configure_mock(side_effect=[item1, item2])
        writer.mock_buffer_value.configure_mock(side_effect=None)
        writer.mock_clear_buffer.configure_mock(side_effect=None)

        writer.write("tag1", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        elapsed_handlers = list(writer.timer.elapsed)
        writer.clear_buffered_writes()
        writer.write("tag2", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)

        # Simulate queuing the timer event in parallel to ClearBufferedWrites
        # by raising the event using the handlers that were there earlier.
        # (The second write should have replaced them with *new* event handlers. It
        # should also stop the original timer, but if the timer is already elapsing, it
        # should be ignored.)
        # The strict mock will assert the writes were never sent.
        assert elapsed_handlers is not None
        for h in elapsed_handlers:
            h()

    def test__writer_closed__flush_timer_elapsed__writes_not_sent(self):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())
        item = object()

        writer.mock_create_item.configure_mock(side_effect=None, return_value=item)
        writer.mock_buffer_value.configure_mock(side_effect=None)
        can_start_property = PropertyMock(return_value=True)
        type(writer.timer).can_start = can_start_property

        with writer:
            writer.write("tag", tbase.DataType.DOUBLE, 1.1, timestamp=self.timestamp)
        writer.trigger_flush_event()
        # The strict mock will assert the writes were never sent.

    @pytest.mark.asyncio
    async def test__writer_closed__methods_called__raises(self):
        writer = self.MockBufferedTagWriter(None, 2, MockManualResetTimer())
        with writer:
            pass

        with pytest.raises(ReferenceError):
            writer.clear_buffered_writes()
        with pytest.raises(ReferenceError):
            writer.send_buffered_writes()
        with pytest.raises(ReferenceError):
            await writer.send_buffered_writes_async()
        with pytest.raises(ReferenceError):
            writer.write("tag", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp)
        with pytest.raises(ReferenceError):
            await writer.write_async(
                "tag", tbase.DataType.BOOLEAN, False, timestamp=self.timestamp
            )

    class MockBufferedTagWriter(tbase.BufferedTagWriter):
        def __init__(self, stamper=None, buffer_size=None, flush_timer=None):
            assert buffer_size is not None
            super().__init__(
                stamper or SystemTimeStamper(),
                buffer_size,
                flush_timer or ManualResetTimer.null_timer,
            )
            self._timer = flush_timer
            self._time_stamper = stamper

            self.mock_buffer_value = Mock(side_effect=NotImplementedError)
            self.mock_clear_buffer = Mock(side_effect=NotImplementedError)
            self.mock_copy_buffer = Mock(side_effect=NotImplementedError)
            self.mock_create_item = Mock(side_effect=NotImplementedError)
            self.mock_send_writes = Mock(side_effect=NotImplementedError)
            self.mock_send_writes = Mock(side_effect=NotImplementedError)
            self.mock_send_writes_async = Mock(side_effect=NotImplementedError)

        @property
        def timer(self):
            return self._timer

        @property
        def time_stamper(self):
            return self._time_stamper

        def trigger_flush_event(self):
            self._timer.elapsed()

        def _buffer_value(self, *args, **kwargs):
            return self.mock_buffer_value(*args, **kwargs)

        def _clear_buffer(self, *args, **kwargs):
            return self.mock_clear_buffer(*args, **kwargs)

        def _copy_buffer(self, *args, **kwargs):
            return self.mock_copy_buffer(*args, **kwargs)

        def _create_item(self, *args, **kwargs):
            return self.mock_create_item(*args, **kwargs)

        def _send_writes(self, *args, **kwargs):
            return self.mock_send_writes(*args, **kwargs)

        async def _send_writes_async(self, *args, **kwargs):
            return self.mock_send_writes_async(*args, **kwargs)
