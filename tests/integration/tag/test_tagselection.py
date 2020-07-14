# -*- coding: utf-8 -*-

import contextlib
import math
import sys
import time
from datetime import datetime, timezone

import pytest  # type: ignore
from systemlink.clients import tag as tbase

from .mixins import CloudMixin, ServerMixin


class TagSelectionTests:
    @pytest.fixture(autouse=True)
    def _gen_tags(self, request, generate_each_tag_type):
        request.cls._tags, request.cls._path_prefix = generate_each_tag_type()

    def test__create_selection_from_tags__paths_and_tags_are_correct(self):
        with self.tag_manager.create_selection(self._tags) as selection:
            paths = [t.path for t in self._tags]
            assert sorted(paths) == sorted(selection.paths)
            assert sorted(paths) == sorted(selection.metadata.keys())

    def test__create_selection_from_paths__paths_and_tags_are_correct(self):
        path_query = self._path_prefix + "*"
        with self.tag_manager.open_selection([path_query]) as selection:
            assert 1 == len(selection.paths)
            assert path_query == selection.paths[0]
            assert sorted([t.path for t in self._tags]) == sorted(
                selection.metadata.keys()
            )

    def test__create_empty_selection__has_no_tags(self):
        with self.tag_manager.create_selection([]) as selection:
            selection.refresh()
            assert 0 == len(selection.paths)
            assert 0 == len(selection.metadata)
            assert 0 == len(selection.values)

    def test__selection_created_for_missing_tag__refresh__selection_has_tag_iff_it_exists(
        self, generate_tag_path
    ):
        missing_path = generate_tag_path(suffix="missing")

        with self.tag_manager.open_selection([missing_path]) as selection:
            assert 0 == len(selection.metadata)
            assert 0 == len(selection.values)

            self.tag_manager.open(missing_path, tbase.DataType.INT32, create=True)
            selection.refresh()

            assert 1 == len(selection.metadata)
            assert 1 == len(selection.values)
            assert missing_path == list(selection.metadata.values())[0].path

            self.tag_manager.delete([missing_path])
            selection.refresh()

            assert 0 == len(selection.metadata)
            assert 0 == len(selection.values)

    def test__some_tags_deleted_or_added__refresh_metadata__tag_list_is_correct(self):
        with self.tag_manager.create_selection(
            self._tags[: len(self._tags) // 2]
        ) as selection:
            selection.delete_tags_from_server()
            selection.add_tags(self._tags)
            selection.refresh_metadata()

            assert sorted(
                [t.path for t in self._tags[len(self._tags) // 2 :]]
            ) == sorted(selection.metadata.keys())

            self.tag_manager.update(self._tags)
            selection.refresh_metadata()

            assert sorted([t.path for t in self._tags]) == sorted(
                selection.metadata.keys()
            )

    def test__write_and_read_some_or_all_selection_tags__values_are_correct(self):
        assert (
            len(self._tags) == 6
        ), "Test needs to be updated to add additional data types"

        with contextlib.ExitStack() as exit_stack:
            selection = exit_stack.enter_context(
                self.tag_manager.create_selection(self._tags)
            )
            writer = exit_stack.enter_context(
                self.tag_manager.create_writer(buffer_size=len(self._tags))
            )

            tags = {t.data_type.name: t for t in self._tags}

            writer.write(tags["BOOLEAN"].path, tags["BOOLEAN"].data_type, True)
            writer.write(tags["DOUBLE"].path, tags["DOUBLE"].data_type, math.pi)
            writer.send_buffered_writes()

            for i in range(10):
                bool_value = selection.read(
                    tags["BOOLEAN"].path,
                    include_timestamp=False,
                    include_aggregates=False,
                ).value
                double_value = selection.read(
                    tags["DOUBLE"].path,
                    include_timestamp=False,
                    include_aggregates=False,
                ).value

                if bool_value is not None and double_value is not None:
                    break

                time.sleep(0.25)
                selection.refresh_values()
            else:
                assert bool_value is not None
                assert double_value is not None

            assert selection.read(tags["BOOLEAN"].path).value is True
            assert selection.read(tags["DATE_TIME"].path) is None
            assert math.pi == selection.read(tags["DOUBLE"].path).value
            assert selection.read(tags["INT32"].path) is None
            assert selection.read(tags["STRING"].path) is None
            assert selection.read(tags["UINT64"].path) is None

            date_value = datetime.now(timezone.utc)
            int_value = -13
            string_value = "hello there"
            uint64_value = 2 ** 31 + 3

            writer.write(tags["BOOLEAN"].path, tags["BOOLEAN"].data_type, False)
            writer.write(
                tags["DATE_TIME"].path, tags["DATE_TIME"].data_type, date_value
            )
            writer.write(tags["INT32"].path, tags["INT32"].data_type, int_value)
            writer.write(tags["STRING"].path, tags["STRING"].data_type, string_value)
            writer.write(tags["UINT64"].path, tags["UINT64"].data_type, uint64_value)
            writer.send_buffered_writes()

            for i in range(10):
                selection.refresh_values()
                if all(selection.read(t.path) is not None for t in tags.values()):
                    break

                time.sleep(0.1)
            else:
                assert all(selection.read(t.path) is not None for t in tags.values())

            assert selection.read(tags["BOOLEAN"].path).value is False
            assert date_value == selection.read(tags["DATE_TIME"].path).value
            assert int_value == selection.read(tags["INT32"].path).value
            assert string_value == selection.read(tags["STRING"].path).value
            assert uint64_value == selection.read(tags["UINT64"].path).value

    def test__reset_aggregates__aggregate_values_are_correct(self):
        with contextlib.ExitStack() as exit_stack:
            selection = exit_stack.enter_context(
                self.tag_manager.create_selection(self._tags)
            )
            writer = exit_stack.enter_context(
                self.tag_manager.create_writer(buffer_size=1)
            )

            dbl_tag = [t for t in self._tags if t.data_type == tbase.DataType.DOUBLE][0]
            writer.write(dbl_tag.path, dbl_tag.data_type, -sys.float_info.max / 2)
            writer.write(dbl_tag.path, dbl_tag.data_type, sys.float_info.max / 2)

            for i in range(10):
                value = self.tag_manager.read(dbl_tag.path).value

                if value == sys.float_info.max / 2:
                    break

                time.sleep(0.25)
                selection.refresh_values()
            else:
                assert sys.float_info.max / 2

            value = self.tag_manager.read(
                dbl_tag.path, include_timestamp=False, include_aggregates=True
            )

            assert value is not None
            assert value.count is not None
            assert 2 == value.count
            assert -sys.float_info.max / 2 == value.min
            assert sys.float_info.max / 2 == value.max

            selection.reset_aggregates()
            selection.refresh_values()
            value = self.tag_manager.read(
                dbl_tag.path, include_timestamp=False, include_aggregates=True
            )
            assert value is not None
            assert sys.float_info.max / 2 == value.value
            assert value.count is not None
            assert 1 == value.count
            assert sys.float_info.max / 2 == value.min
            assert sys.float_info.max / 2 == value.max


class TestTagSelectionCloud(TagSelectionTests, CloudMixin):
    pass


class TestTagSelectionServer(TagSelectionTests, ServerMixin):
    pass
