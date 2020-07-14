# -*- coding: utf-8 -*-

import math
import random
import sys
import time
from datetime import datetime, timedelta, timezone

import pytest  # type: ignore
from systemlink.clients import core, tag as tbase

from .mixins import CloudMixin, ServerMixin


class TagManagerTests:
    def test__write_read_bool_tag__values_are_correct(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.BOOLEAN)
            tag.collect_aggregates = True

            self.tag_manager.update([tag])
            self.internal_test_write_and_read_tag(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                value_to_write=True,
            )

    def test__write_read_date_time_tag__values_are_correct(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.DATE_TIME)
            tag.collect_aggregates = True

            self.tag_manager.update([tag])
            self.internal_test_write_and_read_tag(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                value_to_write=datetime.now(timezone.utc),
            )

    def test__write_read_double_tag__values_are_correct(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.DOUBLE)
            tag.collect_aggregates = True

            self.tag_manager.update([tag])
            aggregates = self.internal_test_write_and_read_tag(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                value_to_write=math.pi,
            )

            assert math.pi == aggregates.min
            assert math.pi == aggregates.max
            assert math.pi == aggregates.mean

    def test__write_read_int_tag__values_are_correct(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.INT32)
            tag.collect_aggregates = True

            min_int = -(2 ** 31)
            self.tag_manager.update([tag])
            aggregates = self.internal_test_write_and_read_tag(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                value_to_write=min_int,
            )

            assert min_int == aggregates.min
            assert min_int == aggregates.max
            assert min_int == aggregates.mean

    def test__write_read_string_tag__values_are_correct(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.STRING)
            tag.collect_aggregates = True

            self.tag_manager.update([tag])
            self.internal_test_write_and_read_tag(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                value_to_write="testing this tag value",
            )

    def test__write_read_uint64_tag__values_are_correct(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.UINT64)
            tag.collect_aggregates = True

            value = 2 ** 64 - 1
            self.tag_manager.update([tag])
            aggregates = self.internal_test_write_and_read_tag(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                value_to_write=value,
            )

            assert value == aggregates.min
            assert value == aggregates.max
            assert math.isclose(value, aggregates.mean)

    def test__set_double_values__aggregate_values_are_correct(self, generate_tag_path):
        min = -random.random() * sys.float_info.max / 2
        max = random.random() * sys.float_info.max / 2
        mean = (min + max) / 3

        with self.tag_manager.create_writer(buffer_size=3) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.DOUBLE)
            tag.collect_aggregates = True

            self.tag_manager.update([tag])
            aggregates = self.internal_test_numeric_aggregates(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                mean,
                (0.0, max, min),
            )

            assert math.isclose(min, aggregates.min), (min, aggregates.min)
            assert math.isclose(max, aggregates.max), (max, aggregates.max)

    def test__set_int_values__aggregate_values_are_correct(self, generate_tag_path):
        min = random.randrange(-(2 ** 31), 0)
        max = random.randrange(0, 2 ** 31 - 1)
        mean = (min + max) / 3.0

        with self.tag_manager.create_writer(buffer_size=3) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.INT32)
            tag.collect_aggregates = True

            self.tag_manager.update([tag])
            aggregates = self.internal_test_numeric_aggregates(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                mean,
                (min, 0, max),
            )

            assert min == aggregates.min
            assert max == aggregates.max

    def test__uint64_aggregates(self, generate_tag_path):
        min = random.randrange(0, 2 ** 31)
        max = random.randrange(2 ** 31, 2 ** 32)
        mean = (min + max + 2 ** 31) / 3.0

        with self.tag_manager.create_writer(buffer_size=3) as writer:
            tag = tbase.TagData(generate_tag_path(), tbase.DataType.UINT64)
            tag.collect_aggregates = True

            self.tag_manager.update([tag])
            aggregates = self.internal_test_numeric_aggregates(
                tag,
                writer,
                tbase.TagValueReader(self.tag_manager, tag),
                mean,
                (max, min, 2 ** 31),
            )

            assert min == aggregates.min
            assert max == aggregates.max

    def test__collect_aggregates_False__aggregates_is_None(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = self.tag_manager.open(
                generate_tag_path(), tbase.DataType.DOUBLE, create=True
            )
            writer.write(tag.path, tag.data_type, math.e)

            for i in range(10):
                value = self.tag_manager.read(
                    tag.path, include_timestamp=False, include_aggregates=True
                )
                if value.value == math.e:
                    break
            else:
                assert value.value == math.e

            assert value.count is None

    def test__special_tag_paths_used__apis_work(self, generate_tag_path):
        paths = ["basic", "space path", "slash/path", "underscore_path"]

        with self.tag_manager.create_writer(buffer_size=1) as writer:
            for path in paths:
                tag = self.tag_manager.open(
                    generate_tag_path(path), tbase.DataType.DOUBLE, create=True
                )
                tag.collect_aggregates = True
                self.tag_manager.update(
                    updates=[
                        tbase.TagDataUpdate.from_tagdata(
                            tag, tbase.TagUpdateFields.COLLECT_AGGREGATES
                        )
                    ]
                )
                self.internal_test_write_and_read_tag(
                    tag, writer, tbase.TagValueReader(self.tag_manager, tag), 3.0,
                )
                self.tag_manager.delete([tag])

    def test__update_metadata__queried_metadata_is_correct(self, generate_tag_path):
        tag = tbase.TagData(
            generate_tag_path(),
            tbase.DataType.DOUBLE,
            ["keyword1", "keyword2"],
            {"prop1": "value1", "prop2": "value2"},
        )

        self.tag_manager.update([tag])
        opened_tag = self.tag_manager.open(tag.path)

        assert opened_tag.collect_aggregates is False
        assert tbase.DataType.DOUBLE == opened_tag.data_type
        assert sorted(tag.keywords) == sorted(opened_tag.keywords)
        assert tag.path == opened_tag.path
        assert sorted(tag.properties.items()) == sorted(opened_tag.properties.items())
        assert opened_tag.retention_count is None
        assert opened_tag.retention_days is None
        assert tbase.RetentionType.NONE == opened_tag.retention_type

        tag.collect_aggregates = True
        tag.set_retention_count(30)
        tag.keywords.append("keyword3")
        tag.properties["prop1"] = "edited"
        self.tag_manager.update([tag])
        self.tag_manager.refresh([opened_tag])

        assert opened_tag.collect_aggregates is True
        assert tbase.DataType.DOUBLE == opened_tag.data_type
        assert sorted(tag.keywords) == sorted(opened_tag.keywords)
        assert tag.path == opened_tag.path
        assert sorted(tag.properties.items()) == sorted(opened_tag.properties.items())
        assert 30 == opened_tag.retention_count
        assert opened_tag.retention_days is None
        assert tbase.RetentionType.COUNT == opened_tag.retention_type

    def test__merge_metadata__queried_metadata_is_correct(self, generate_tag_path):
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        tag = tbase.TagData(
            generate_tag_path(), tbase.DataType.DOUBLE, keywords, properties
        )

        self.tag_manager.update([tag])
        opened_tag = self.tag_manager.open(tag.path)

        assert opened_tag.collect_aggregates is False
        assert tbase.DataType.DOUBLE == opened_tag.data_type
        assert sorted(keywords) == sorted(opened_tag.keywords)
        assert tag.path == opened_tag.path
        assert sorted(properties.items()) == sorted(opened_tag.properties.items())
        assert opened_tag.retention_count is None
        assert opened_tag.retention_days is None
        assert tbase.RetentionType.NONE == opened_tag.retention_type

        tag.collect_aggregates = True
        tag.set_retention_count(50)
        tag.keywords[:] = ["keyword3"]
        tag.properties.clear()
        tag.properties.update({"prop1": "edited", "prop3": "value3"})
        self.tag_manager.update(
            updates=[tbase.TagDataUpdate.from_tagdata(tag, tbase.TagUpdateFields.ALL)]
        )
        self.tag_manager.refresh([opened_tag])

        keywords.append("keyword3")
        properties["prop1"] = "edited"
        properties["prop3"] = "value3"
        assert opened_tag.collect_aggregates is True
        assert tbase.DataType.DOUBLE == opened_tag.data_type
        assert sorted(keywords) == sorted(opened_tag.keywords)
        assert tag.path == opened_tag.path
        assert sorted(properties.items()) == sorted(opened_tag.properties.items())
        assert 50 == opened_tag.retention_count
        assert opened_tag.retention_days is None
        assert tbase.RetentionType.COUNT == opened_tag.retention_type

        # First update the collect aggregates and retention settings
        # then do a merge that excludes those properties and verify
        # they are unmodified.
        opened_tag.collect_aggregates = False
        opened_tag.set_retention_days(30)
        tag.properties["prop4"] = "value4"
        self.tag_manager.update([opened_tag])
        self.tag_manager.update(
            updates=[
                tbase.TagDataUpdate.from_tagdata(
                    tag,
                    tbase.TagUpdateFields.KEYWORDS | tbase.TagUpdateFields.PROPERTIES,
                )
            ]
        )
        self.tag_manager.refresh([opened_tag])

        properties["prop4"] = "value4"
        assert opened_tag.collect_aggregates is False
        assert tbase.DataType.DOUBLE == opened_tag.data_type
        assert sorted(keywords) == sorted(opened_tag.keywords)
        assert tag.path == opened_tag.path
        assert sorted(properties.items()) == sorted(opened_tag.properties.items())
        assert 30 == opened_tag.retention_days
        assert tbase.RetentionType.DURATION == opened_tag.retention_type
        assert 50 == opened_tag.retention_count

    def test__change_data_type__raises(self, generate_tag_path):
        tag = self.tag_manager.open(
            generate_tag_path(), tbase.DataType.BOOLEAN, create=True
        )
        tag.data_type = tbase.DataType.DATE_TIME
        with pytest.raises(core.ApiException) as ex:
            self.tag_manager.update([tag])

        assert ex.value.error is not None
        assert ex.value.error.code in (
            -251041,  # Skyline.OneOrMoreErrorsOccurred
            -251907,  # Tag.ConflictingTagTypes
        )

        with pytest.raises(core.ApiException) as ex:
            self.tag_manager.open(tag.path, tbase.DataType.DOUBLE, create=True)
        assert "type" in ex.value.message

    def test__write_wrong_data_type__write_ignored(self, generate_tag_path):
        with self.tag_manager.create_writer(buffer_size=1) as writer:
            tag = self.tag_manager.open(
                generate_tag_path(), tbase.DataType.DOUBLE, create=True
            )
            writer.write(tag.path, tbase.DataType.INT32, 7)
            assert self.tag_manager.read(tag.path) is None

    def test__run_queries__results_are_correct(self, generate_tag_paths):
        num_tags = 10
        even_paths = []
        odd_paths = []
        paths, path_prefix = generate_tag_paths(num_tags)
        tags = [tbase.TagData(p, tbase.DataType.INT32) for p in paths]

        for x, tag in enumerate(tags):
            odd_even = ""

            if x % 2 == 0:
                odd_even = "even"
                even_paths.append(tag.path)
            else:
                odd_even = "odd"
                odd_paths.append(tag.path)

            tag.keywords.append(odd_even)
            tag.properties["index"] = str(x)
            tag.properties["oddEven"] = odd_even

        self.tag_manager.update(tags)

        # Path query
        half_paths = paths[: num_tags // 2]
        self.internal_test_query_result(
            self.tag_manager.query(half_paths), half_paths, num_tags // 2
        )

        # Wildcard query
        self.internal_test_query_result(
            self.tag_manager.query([path_prefix + "*"]), paths, len(paths)
        )

        # Keyword query
        self.internal_test_query_result(
            self.tag_manager.query(paths, keywords=["odd"], properties=None),
            odd_paths,
            len(odd_paths),
        )

        # Property query
        self.internal_test_query_result(
            self.tag_manager.query(
                paths, keywords=None, properties={"oddEven": "even"}
            ),
            even_paths,
            len(even_paths),
        )

        # Pages
        self.internal_test_query_result(
            self.tag_manager.query(paths, skip=1, take=2),
            paths,
            page_size=2,
            skip=1,
            expected_pages=math.ceil((num_tags - 1) / 2.0),
        )

    @classmethod
    def internal_test_query_result(
        cls, query, expected_paths, page_size, skip=0, expected_pages=1
    ):
        expected_list = list(expected_paths)
        assert len(expected_list) == query.total_count

        pages = list(query)
        assert expected_pages == len(pages)
        assert all(len(page) == page_size for page in pages[:-1])
        paths = [tag.path for page in pages for tag in page]

        expected_list[0:skip] = []
        assert sorted(expected_list) == sorted(paths)
        assert expected_pages == len(pages)

    @classmethod
    def internal_test_write_and_read_tag(cls, tag, writer, reader, value_to_write):
        # Shouldn't start with a value.
        assert reader.read(include_timestamp=True, include_aggregates=True) is None

        # Write the value.
        writer.write(tag.path, tag.data_type, value_to_write)

        # Read may not return the value immediately.
        for i in range(10):
            value = reader.read(include_timestamp=True, include_aggregates=True)
            if value is not None:
                break
            time.sleep(0.1)
        else:
            assert value is not None

        # value should be what we wrote.
        assert value_to_write == value.value
        now = datetime.now(timezone.utc)
        assert value.timestamp < now
        assert now - value.timestamp < timedelta(days=1)
        assert value.count is not None
        assert 1 == value.count
        return value

    @classmethod
    def internal_test_numeric_aggregates(cls, tag, writer, reader, mean, values):
        # Shouldn't start with a value.
        assert reader.read(include_timestamp=False, include_aggregates=True) is None

        # Write each value.
        for value in values:
            writer.write(tag.path, tag.data_type, value)

        # Read until each value has been seen.
        num_values = len(values)
        for i in range(10):
            value = reader.read(include_timestamp=False, include_aggregates=True)
            if value is not None and value.count == num_values:
                break
            time.sleep(0.1)
        else:
            assert value is not None and num_values == value.count

        assert value is not None

        # Check the results.
        if isinstance(value, float):
            assert math.isclose(values[-1], value), (values[-1], value)
        else:
            assert values[-1] == value.value

        assert math.isclose(mean, value.mean), (mean, value.mean)
        return value


class TestTagManagerCloud(TagManagerTests, CloudMixin):
    pass


class TestTagManagerServer(TagManagerTests, ServerMixin):
    pass
