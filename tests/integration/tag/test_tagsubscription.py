# -*- coding: utf-8 -*-

import contextlib
import math
import time
from datetime import datetime, timedelta, timezone

import pytest  # type: ignore
from systemlink.clients import tag as tbase

from .mixins import CloudMixin, ServerMixin


class TagSubscriptionTests:
    @pytest.fixture(autouse=True)
    def _gen_tags(self, request, generate_each_tag_type):
        request.cls._tags, request.cls._path_prefix = generate_each_tag_type()

    def test__create_and_destroy_subscription__no_error(self):
        with contextlib.ExitStack() as exit_stack:
            selection = exit_stack.enter_context(
                self.tag_manager.create_selection(self._tags)
            )
            subscription = exit_stack.enter_context(selection.create_subscription())
            assert subscription is not None

    def test__subscribed_values_updated__subscription_receives_events(self):
        assert (
            len(self._tags) == 6
        ), "Test needs to be updated to add additional data types"

        values = set()
        polling_interval = timedelta(milliseconds=500)
        date_value = datetime.now(timezone.utc)
        bool_value = False
        double_value = math.pi
        int_value = -13
        string_value = "hello there"
        uint64_value = 2 ** 31 + 3

        with contextlib.ExitStack() as exit_stack:
            selection = exit_stack.enter_context(
                self.tag_manager.create_selection(self._tags)
            )
            subscription = exit_stack.enter_context(
                selection.create_subscription(update_interval=polling_interval)
            )
            writer = exit_stack.enter_context(
                self.tag_manager.create_writer(buffer_size=2)
            )

            subscription.tag_changed += lambda tag, reader: values.add((tag, reader))

            tags = {t.data_type.name: t for t in self._tags}
            writer.write(tags["BOOLEAN"].path, tags["BOOLEAN"].data_type, bool_value)
            writer.write(
                tags["DATE_TIME"].path, tags["DATE_TIME"].data_type, date_value
            )
            writer.write(tags["DOUBLE"].path, tags["DOUBLE"].data_type, double_value)
            writer.write(tags["INT32"].path, tags["INT32"].data_type, int_value)
            writer.write(tags["STRING"].path, tags["STRING"].data_type, string_value)
            writer.write(tags["UINT64"].path, tags["UINT64"].data_type, uint64_value)
            writer.send_buffered_writes()

            # Wait for the subscription events to come in.
            for _ in range(10):
                if len(self._tags) == len(values):
                    break
                time.sleep(polling_interval.total_seconds())
            else:
                assert len(self._tags) == len(values)

        # Exactly one of each data type.
        assert len(self._tags) == len(
            values
        )  # len(set(t.tag.data_type for t in values))

        for (tag, reader) in values:
            assert reader is not None
            if tag.data_type == tbase.DataType.DOUBLE:
                assert double_value == reader.read().value
                break
            elif tag.data_type == tbase.DataType.INT32:
                assert int_value == reader.read().value
                break
            elif tag.data_type == tbase.DataType.STRING:
                assert string_value == reader.read().value
                break
            elif tag.data_type == tbase.DataType.BOOLEAN:
                assert bool_value == reader.read().value
                break
            elif tag.data_type == tbase.DataType.UINT64:
                assert uint64_value == reader.read().value
                break
            elif tag.data_type == tbase.DataType.DATE_TIME:
                assert date_value == reader.read().value
                break
            else:
                assert False, "Unknown data type {}".format(tag.data_type)
                break

    @pytest.mark.slow
    def test__subscription_outlives_heartbeat_interval__events_still_received(self):
        # Ensure the last write happens after at least one heartbeat must have been sent.
        heartbeat_interval = 60
        num_writes = 5
        polling_interval = timedelta(seconds=heartbeat_interval / (num_writes - 1))

        with contextlib.ExitStack() as exit_stack:
            selection = exit_stack.enter_context(
                self.tag_manager.create_selection(self._tags)
            )
            subscription = exit_stack.enter_context(selection.create_subscription())
            writer = exit_stack.enter_context(
                self.tag_manager.create_writer(buffer_size=1)
            )

            int_tag = [t for t in self._tags if t.data_type == tbase.DataType.INT32][0]
            tag_changes = []
            subscription.tag_changed += lambda tag, reader: tag_changes.append(
                (tag, reader)
            )

            for x in range(num_writes):
                writer.write(int_tag.path, int_tag.data_type, x)

                for _ in range(2):
                    if 1 == len(tag_changes):
                        break
                    time.sleep(1 + polling_interval.total_seconds())
                else:
                    assert 1 == len(tag_changes)

                tag, reader = tag_changes.pop(0)
                assert x == reader.read().value


class TestTagSubscriptionCloud(TagSubscriptionTests, CloudMixin):
    pass


class TestTagSubscriptionServer(TagSubscriptionTests, ServerMixin):
    pass
