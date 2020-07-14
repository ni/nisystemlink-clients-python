import datetime
from unittest import mock
from unittest.mock import Mock

import pytest  # type: ignore
from systemlink.clients.tag import DataType, TagData, TagSelection, TagSubscription
from systemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)


class TestTagSelection:
    def test__invalid_metadata__constructed__raises(self):
        with pytest.raises(ValueError):
            self.MockTagSelection(None)

        with pytest.raises(ValueError):
            self.MockTagSelection([None])

        with pytest.raises(ValueError):
            self.MockTagSelection([TagData("")])

        with pytest.raises(ValueError):
            self.MockTagSelection([TagData("tag"), TagData("tag")])

    def test__constructed_with_metadata__paths_come_from_tags_without_query(self):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        tags = [
            TagData(path1),
            TagData(path2, DataType.DATE_TIME),
            TagData(path3, DataType.DOUBLE),
        ]
        paths = [path1, path2, path3]
        selection = self.MockTagSelection(tags)

        assert paths == list(sorted(selection.paths))
        assert sorted(paths) == sorted(selection.metadata.keys())
        assert sorted(tags, key=(lambda t: t.path)) == sorted(
            selection.metadata.values(), key=(lambda t: t.path)
        )

    def test__constructed_with_metadata__appropriate_readers_created(self):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        path4 = "tag4"
        path5 = "tag5"
        path6 = "tag6"
        path7 = "tag7"
        tags = [
            TagData(path1),
            TagData(path2, DataType.BOOLEAN),
            TagData(path3, DataType.DATE_TIME),
            TagData(path4, DataType.DOUBLE),
            TagData(path5, DataType.INT32),
            TagData(path6, DataType.STRING),
            TagData(path7, DataType.UINT64),
        ]
        paths = [path1, path2, path3, path4, path5, path6, path7]
        selection = self.MockTagSelection(tags)

        # The first tag has unknown data type and should not appear in the values collection.
        assert paths[1:] == list(sorted(selection.values.keys()))
        assert selection.values[path2].data_type == DataType.BOOLEAN
        assert selection.values[path3].data_type == DataType.DATE_TIME
        assert selection.values[path4].data_type == DataType.DOUBLE
        assert selection.values[path5].data_type == DataType.INT32
        assert selection.values[path6].data_type == DataType.STRING
        assert selection.values[path7].data_type == DataType.UINT64

        for key, value in selection.values.items():
            assert key == value.path

    def test__constructed_with_invalid_query_data__raises(self):
        with pytest.raises(ValueError):
            self.MockTagSelection(None, [""] * 0)

        with pytest.raises(ValueError):
            self.MockTagSelection([None])

        with pytest.raises(ValueError):
            self.MockTagSelection([TagData("")])

        with pytest.raises(ValueError):
            self.MockTagSelection([TagData("tag"), TagData("tag")])

    def test__constructed_with_metadata_and_queries__uses_given_data_without_additional_query(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        queries = ["tag1", "tag*"]
        tags = [
            TagData(path1),
            TagData(path2, DataType.DATE_TIME),
            TagData(path3, DataType.DOUBLE),
        ]
        tag_paths = [path1, path2, path3]
        selection = self.MockTagSelection(tags, queries)

        assert sorted(queries) == sorted(selection.paths)
        assert sorted(tag_paths) == sorted(selection.metadata.keys())
        assert sorted(tags, key=(lambda t: t.path)) == sorted(
            selection.metadata.values(), key=(lambda t: t.path)
        )

    def test__constructed_with_metadata_and_queries__appropriate_readers_created(self):
        path1 = "tag1"
        path2 = "tag2"
        path3 = "tag3"
        path4 = "tag4"
        path5 = "tag5"
        path6 = "tag6"
        path7 = "tag7"
        tags = [
            TagData(path1),
            TagData(path2, DataType.BOOLEAN),
            TagData(path3, DataType.DATE_TIME),
            TagData(path4, DataType.DOUBLE),
            TagData(path5, DataType.INT32),
            TagData(path6, DataType.STRING),
            TagData(path7, DataType.UINT64),
        ]
        reader_paths = [path2, path3, path4, path5, path6, path7]
        selection = self.MockTagSelection(tags, ["tag*"])

        # The tag with an unknown data type should not appear in the values collection.
        assert reader_paths == list(sorted(selection.values.keys()))
        assert selection.values[path2].data_type == DataType.BOOLEAN
        assert selection.values[path3].data_type == DataType.DATE_TIME
        assert selection.values[path4].data_type == DataType.DOUBLE
        assert selection.values[path5].data_type == DataType.INT32
        assert selection.values[path6].data_type == DataType.STRING
        assert selection.values[path7].data_type == DataType.UINT64

        for key, value in selection.values.items():
            assert key == value.path

    def test__invalid_tags__add_tags__raises_without_making_changes(self):
        selection = self.MockTagSelection([TagData] * 0)
        with pytest.raises(ValueError):
            selection.add_tags([None])
        with pytest.raises(ValueError):
            selection.add_tags([TagData("tag"), None])
        with pytest.raises(ValueError):
            selection.add_tags([TagData("tag"), TagData("")])
        # The strict mock will assert that _on_paths_changed was never called.

    def test__add_tags__updates_paths(self):
        path1 = "tag1"
        path2 = "tag2"
        paths = [path1, path2]
        queries = ["tag*"]
        selection = self.MockTagSelection([TagData(path1)], queries)
        selection.mock_on_paths_changed.configure_mock(side_effect=None)

        selection.add_tags([TagData(path1), TagData(path2)])
        assert sorted(paths + queries) == sorted(selection.paths)
        selection.mock_on_paths_changed.assert_called_once_with()

    def test__add_tags__updates_metadata_without_overwriting(self):
        path1 = "tag1"
        path2 = "tag2"
        tag1 = TagData(path1, DataType.BOOLEAN)
        tag2 = TagData(path2, DataType.DOUBLE)
        paths = [path1, path2]
        tags = [tag1, tag2]
        selection = self.MockTagSelection([tag1], ["tag*"])

        selection.mock_on_paths_changed.configure_mock(side_effect=None)
        # path1's updated DataType should be ignored
        selection.add_tags([TagData(path1, DataType.DATE_TIME), tag2])

        assert paths == sorted(selection.metadata.keys())
        assert sorted(tags, key=(lambda t: t.path)) == sorted(
            selection.metadata.values(), key=(lambda t: t.path)
        )
        selection.mock_on_paths_changed.assert_called_once_with()

    def test__clear_tags__all_collections_emptied(self):
        selection = self.MockTagSelection([TagData("tag1", DataType.BOOLEAN)], ["tag*"])
        selection.mock_on_paths_changed.configure_mock(side_effect=None)
        selection.clear_tags()

        assert 0 == len(selection.paths)
        assert 0 == len(selection.metadata)
        assert 0 == len(selection.values)
        selection.mock_on_paths_changed.assert_called_once_with()

    def test__close_twice__close_internal_called_once(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_close_internal.configure_mock(side_effect=None)
        selection.close()
        selection.close()
        selection.mock_close_internal.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__close_async_twice__close_internal_async_called_once(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_close_internal_async.configure_mock(side_effect=None)
        await selection.close_async()
        await selection.close_async()
        selection.mock_close_internal_async.assert_called_once_with()

    def test__create_subscription__given_interval_used_if_valid(self):
        update_interval = datetime.timedelta(seconds=60)
        mock_subscription1 = Mock(TagSubscription)
        mock_subscription2 = Mock(TagSubscription)
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_create_subscription_internal.configure_mock(
            side_effect=[mock_subscription1, mock_subscription2]
        )

        assert mock_subscription1 is selection.create_subscription()
        assert mock_subscription2 is selection.create_subscription(
            update_interval=update_interval
        )
        with pytest.raises(ValueError):
            selection.create_subscription(
                update_interval=datetime.timedelta(seconds=-1)
            )

        assert selection.mock_create_subscription_internal.call_args_list == [
            mock.call(None),
            mock.call(update_interval),
        ]

    @pytest.mark.asyncio
    async def test__create_subscription_async__given_interval_used_if_valid(self):
        update_interval = datetime.timedelta(seconds=60)
        mock_subscription1 = Mock(TagSubscription)
        mock_subscription2 = Mock(TagSubscription)
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_create_subscription_internal_async.configure_mock(
            side_effect=[mock_subscription1, mock_subscription2]
        )

        assert mock_subscription1 is await selection.create_subscription_async()
        assert mock_subscription2 is await selection.create_subscription_async(
            update_interval=update_interval
        )
        with pytest.raises(ValueError):
            await selection.create_subscription_async(
                update_interval=datetime.timedelta(seconds=-1)
            )

        assert selection.mock_create_subscription_internal_async.call_args_list == [
            mock.call(None),
            mock.call(update_interval),
        ]

    def test__delete_tags_from_server__collections_cleared_after_delete(self):
        selection = self.MockTagSelection([TagData("tag1", DataType.BOOLEAN)], ["tag*"])
        selection.mock_delete_tags_from_server_internal.configure_mock(side_effect=None)
        selection.delete_tags_from_server()

        assert 0 == len(selection.metadata)
        assert 0 == len(selection.values)
        selection.mock_delete_tags_from_server_internal.assert_called_once_with()

    def test__delete_tags_from_server__cached_values_for_deleted_tags_removed(self):
        path2 = "tag2"
        selection = self.MockTagSelection([TagData("tag1", DataType.STRING)], ["tag*"])
        selection.mock_on_paths_changed.configure_mock(side_effect=None)
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[
                SerializedTagWithAggregates("tag1", DataType.STRING, "value1"),
                SerializedTagWithAggregates(path2, DataType.STRING, "value2"),
            ],
        )
        selection.mock_delete_tags_from_server_internal.configure_mock(side_effect=None)

        selection.refresh_values()
        assert (
            selection.read(path2, include_timestamp=False, include_aggregates=False)
            is not None
        )
        selection.remove_tags([path2])
        selection.delete_tags_from_server()
        selection.add_tags([TagData(path2, DataType.STRING)])

        assert (
            selection.read(path2, include_timestamp=False, include_aggregates=False)
            is None
        )

    @pytest.mark.asyncio
    async def test__delete_tags_from_server_async__collections_cleared_after_asynchronous_delete(
        self,
    ):
        selection = self.MockTagSelection([TagData("tag1", DataType.BOOLEAN)], ["tag*"])
        selection.mock_delete_tags_from_server_internal_async.configure_mock(
            side_effect=None
        )
        await selection.delete_tags_from_server_async()

        assert 0 == len(selection.metadata)
        assert 0 == len(selection.values)
        selection.mock_delete_tags_from_server_internal_async.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__delete_tags_from_server_async__cached_values_for_deleted_tags_removed(
        self,
    ):
        path2 = "tag2"
        selection = self.MockTagSelection([TagData("tag1", DataType.STRING)], ["tag*"])
        selection.mock_on_paths_changed.configure_mock(side_effect=None)
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[
                SerializedTagWithAggregates("tag1", DataType.STRING, "value1"),
                SerializedTagWithAggregates(path2, DataType.STRING, "value2"),
            ],
        )
        selection.mock_delete_tags_from_server_internal_async.configure_mock(
            side_effect=None
        )

        selection.refresh_values()
        assert (
            await selection.read_async(
                path2, include_timestamp=False, include_aggregates=False
            )
            is not None
        )
        selection.remove_tags([path2])
        await selection.delete_tags_from_server_async()
        selection.add_tags([TagData(path2, DataType.STRING)])

        assert (
            await selection.read_async(
                path2, include_timestamp=False, include_aggregates=False
            )
            is None
        )

    def test__invalid_paths__open_tags__raises(self):
        selection = self.MockTagSelection([TagData] * 0)
        with pytest.raises(ValueError):
            selection.open_tags([None])
        with pytest.raises(ValueError):
            selection.open_tags(["path1", None])
        with pytest.raises(ValueError):
            selection.open_tags(["path1", ""])

    def test__open_tags__paths_added_without_query(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_on_paths_changed.configure_mock(side_effect=None)
        selection.open_tags(["tag1", "tag2"])
        assert ["tag1", "tag2"] == list(sorted(selection.paths))
        selection.mock_on_paths_changed.assert_called_once_with()

    def test__refresh__metadata_updated_and_readers_replaced_where_type_changed(self):
        path1 = "tag1"
        path2 = "tag2"
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        selection = self.MockTagSelection(
            [TagData(path1, DataType.BOOLEAN), TagData(path2, DataType.INT32)]
        )
        selection.mock_read_tag_metadata_and_values.configure_mock(
            side_effect=None,
            return_value=(
                [
                    TagData(path1, DataType.DATE_TIME),
                    TagData(path2, DataType.INT32, keywords, properties),
                ],
                [SerializedTagWithAggregates] * 0,
            ),
        )

        original_reader = selection.values.get(path1)
        assert original_reader
        assert original_reader.data_type == DataType.BOOLEAN
        original_reader = selection.values.get(path2)
        assert original_reader
        assert original_reader.data_type == DataType.INT32

        selection.refresh()

        data = selection.metadata.get(path1)
        assert data
        assert DataType.DATE_TIME == data.data_type
        new_reader = selection.values.get(path1)
        assert new_reader
        assert new_reader.data_type == DataType.DATE_TIME

        data = selection.metadata.get(path2)
        assert data
        assert DataType.INT32 == data.data_type
        assert keywords == sorted(data.keywords)
        assert sorted(properties) == sorted(data.properties)
        new_reader = selection.values.get(path2)
        assert new_reader
        assert original_reader is new_reader

    def test__refresh__metadata_and_readers_added_and_removed(self):
        removed_path = "removed"
        existing_path = "existing"
        added_path = "added"
        selection = self.MockTagSelection(
            [
                TagData(removed_path, DataType.BOOLEAN),
                TagData(existing_path, DataType.INT32),
            ]
        )
        selection.mock_read_tag_metadata_and_values.configure_mock(
            side_effect=None,
            return_value=(
                [
                    TagData(existing_path, DataType.INT32),
                    TagData(added_path, DataType.STRING),
                ],
                [SerializedTagWithAggregates] * 0,
            ),
        )

        selection.refresh()

        assert removed_path not in selection.metadata
        assert removed_path not in selection.values

        data = selection.metadata.get(existing_path)
        assert data
        assert DataType.INT32 == data.data_type
        reader = selection.values.get(existing_path)
        assert reader
        assert reader.data_type == DataType.INT32

        data = selection.metadata.get(added_path)
        assert data
        assert DataType.STRING == data.data_type
        reader = selection.values.get(added_path)
        assert reader
        assert reader.data_type == DataType.STRING

    def test__refresh__values_updated(self):
        value_path = "tag1"
        no_value_path = "tag2"
        tags = [
            TagData(value_path, DataType.INT32),
            TagData(no_value_path, DataType.DATE_TIME),
        ]
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        selection = self.MockTagSelection(tags)
        selection.mock_read_tag_metadata_and_values.configure_mock(
            side_effect=None,
            return_value=(
                tags,
                [
                    SerializedTagWithAggregates(
                        value_path, DataType.INT32, "5", timestamp, 3, "4", "9", 6.0
                    )
                ],
            ),
        )

        selection.refresh()
        value = selection.read(
            value_path, include_timestamp=True, include_aggregates=True
        )

        assert value is not None
        assert DataType.INT32 == value.data_type
        assert 5 == value.value
        assert timestamp == value.timestamp
        assert 3 == value.count
        assert 4 == value.min
        assert 9 == value.max
        assert 6.0 == value.mean
        assert (
            selection.read(
                no_value_path, include_timestamp=True, include_aggregates=True
            )
            is None
        )

    @pytest.mark.asyncio
    async def test__refresh_async__metadata_updated_and_readers_replaced_when_type_changed(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        selection = self.MockTagSelection(
            [TagData(path1, DataType.BOOLEAN), TagData(path2, DataType.INT32)]
        )
        selection.mock_read_tag_metadata_and_values_async.configure_mock(
            side_effect=None,
            return_value=(
                [
                    TagData(path1, DataType.DATE_TIME),
                    TagData(path2, DataType.INT32, keywords, properties),
                ],
                [SerializedTagWithAggregates] * 0,
            ),
        )

        original_reader = selection.values.get(path1)
        assert original_reader
        assert original_reader.data_type == DataType.BOOLEAN
        original_reader = selection.values.get(path2)
        assert original_reader
        assert original_reader.data_type == DataType.INT32

        await selection.refresh_async()

        data = selection.metadata.get(path1)
        assert data
        assert DataType.DATE_TIME == data.data_type
        new_reader = selection.values.get(path1)
        assert new_reader
        assert new_reader.data_type == DataType.DATE_TIME

        data = selection.metadata.get(path2)
        assert data
        assert DataType.INT32 == data.data_type
        assert keywords == sorted(data.keywords)
        assert sorted(properties) == sorted(data.properties)
        new_reader = selection.values.get(path2)
        assert new_reader
        assert original_reader is new_reader

    @pytest.mark.asyncio
    async def test__refresh_async__metadata_and_readers_added_and_removed(self):
        removed_path = "removed"
        existing_path = "existing"
        added_path = "added"
        selection = self.MockTagSelection(
            [
                TagData(removed_path, DataType.BOOLEAN),
                TagData(existing_path, DataType.INT32),
            ]
        )
        selection.mock_read_tag_metadata_and_values_async.configure_mock(
            side_effect=None,
            return_value=(
                [
                    TagData(existing_path, DataType.INT32),
                    TagData(added_path, DataType.STRING),
                ],
                [SerializedTagWithAggregates] * 0,
            ),
        )

        await selection.refresh_async()

        assert removed_path not in selection.metadata
        assert removed_path not in selection.values

        data = selection.metadata.get(existing_path)
        assert data
        assert DataType.INT32 == data.data_type
        reader = selection.values.get(existing_path)
        assert reader
        assert reader.data_type == DataType.INT32

        data = selection.metadata.get(added_path)
        assert data
        assert DataType.STRING == data.data_type
        reader = selection.values.get(added_path)
        assert reader
        assert reader.data_type == DataType.STRING

    @pytest.mark.asyncio
    async def test__refresh_async__values_updated(self):
        value_path = "tag1"
        no_value_path = "tag2"
        tags = [
            TagData(value_path, DataType.INT32),
            TagData(no_value_path, DataType.DATE_TIME),
        ]
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        selection = self.MockTagSelection(tags)
        selection.mock_read_tag_metadata_and_values_async.configure_mock(
            side_effect=None,
            return_value=(
                tags,
                [
                    SerializedTagWithAggregates(
                        value_path, DataType.INT32, "5", timestamp, 3, "4", "9", 6.0
                    )
                ],
            ),
        )

        await selection.refresh_async()
        value = await selection.read_async(
            value_path, include_timestamp=True, include_aggregates=True
        )

        assert value is not None
        assert DataType.INT32 == value.data_type
        assert 5 == value.value
        assert timestamp == value.timestamp
        assert 3 == value.count
        assert 4 == value.min
        assert 9 == value.max
        assert 6.0 == value.mean
        assert (
            await selection.read_async(
                no_value_path, include_timestamp=True, include_aggregates=True
            )
            is None
        )

    def test__refresh_metadata__metadata_updated_and_readers_replaced_when_type_changed(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        selection = self.MockTagSelection(
            [TagData(path1, DataType.BOOLEAN), TagData(path2, DataType.INT32)]
        )
        selection.mock_read_tag_metadata.configure_mock(
            side_effect=None,
            return_value=[
                TagData(path1, DataType.DATE_TIME),
                TagData(path2, DataType.INT32, keywords, properties),
            ],
        )

        original_reader = selection.values.get(path1)
        assert original_reader
        assert original_reader.data_type == DataType.BOOLEAN
        original_reader = selection.values.get(path2)
        assert original_reader
        assert original_reader.data_type == DataType.INT32

        selection.refresh_metadata()

        data = selection.metadata.get(path1)
        assert data
        assert DataType.DATE_TIME == data.data_type
        new_reader = selection.values.get(path1)
        assert new_reader
        assert new_reader.data_type == DataType.DATE_TIME

        data = selection.metadata.get(path2)
        assert data
        assert DataType.INT32 == data.data_type
        assert keywords == sorted(data.keywords)
        assert sorted(properties) == sorted(data.properties)
        new_reader = selection.values.get(path2)
        assert new_reader
        assert original_reader is new_reader

    def test__refresh_metadata__metadata_and_readers_added_and_removed(self):
        removed_path = "removed"
        existing_path = "existing"
        added_path = "added"
        selection = self.MockTagSelection(
            [
                TagData(removed_path, DataType.BOOLEAN),
                TagData(existing_path, DataType.INT32),
            ]
        )
        selection.mock_read_tag_metadata.configure_mock(
            side_effect=None,
            return_value=[
                TagData(existing_path, DataType.INT32),
                TagData(added_path, DataType.STRING),
            ],
        )

        selection.refresh_metadata()

        assert removed_path not in selection.metadata
        assert removed_path not in selection.values

        data = selection.metadata.get(existing_path)
        assert data
        assert DataType.INT32 == data.data_type
        reader = selection.values.get(existing_path)
        assert reader
        assert reader.data_type == DataType.INT32

        data = selection.metadata.get(added_path)
        assert data
        assert DataType.STRING == data.data_type
        reader = selection.values.get(added_path)
        assert reader
        assert reader.data_type == DataType.STRING

    def test__refresh_metadata__cached_values_for_deleted_tags_removed(self):
        path = "tag1"
        tags = [TagData(path, DataType.INT32)]
        selection = self.MockTagSelection(tags)
        selection.mock_read_tag_metadata.configure_mock(
            side_effect=[[TagData] * 0, tags]
        )
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        selection.refresh_values()
        selection.refresh_metadata()
        selection.refresh_metadata()

        assert (
            selection.read(path, include_timestamp=True, include_aggregates=True)
            is None
        )

    @pytest.mark.asyncio
    async def test__refresh_metadata_async__metadata_updated_and_readers_replaced_when_type_changed(
        self,
    ):
        path1 = "tag1"
        path2 = "tag2"
        keywords = ["keyword1", "keyword2"]
        properties = {"prop1": "value1", "prop2": "value2"}
        selection = self.MockTagSelection(
            [TagData(path1, DataType.BOOLEAN), TagData(path2, DataType.INT32)]
        )
        selection.mock_read_tag_metadata_async.configure_mock(
            side_effect=None,
            return_value=(
                [
                    TagData(path1, DataType.DATE_TIME),
                    TagData(path2, DataType.INT32, keywords, properties),
                ]
            ),
        )

        original_reader = selection.values.get(path1)
        assert original_reader
        assert original_reader.data_type == DataType.BOOLEAN
        original_reader = selection.values.get(path2)
        assert original_reader
        assert original_reader.data_type == DataType.INT32

        await selection.refresh_metadata_async()

        data = selection.metadata.get(path1)
        assert data
        assert DataType.DATE_TIME == data.data_type
        new_reader = selection.values.get(path1)
        assert new_reader
        assert new_reader.data_type == DataType.DATE_TIME

        data = selection.metadata.get(path2)
        assert data
        assert DataType.INT32 == data.data_type
        assert keywords == sorted(data.keywords)
        assert sorted(properties) == sorted(data.properties)
        new_reader = selection.values.get(path2)
        assert new_reader
        assert original_reader is new_reader

    @pytest.mark.asyncio
    async def test__refresh_metadata_async__metadata_and_readers_added_and_removed(
        self,
    ):
        removed_path = "removed"
        existing_path = "existing"
        added_path = "added"
        selection = self.MockTagSelection(
            [
                TagData(removed_path, DataType.BOOLEAN),
                TagData(existing_path, DataType.INT32),
            ]
        )
        selection.mock_read_tag_metadata_async.configure_mock(
            side_effect=None,
            return_value=[
                TagData(existing_path, DataType.INT32),
                TagData(added_path, DataType.STRING),
            ],
        )

        await selection.refresh_metadata_async()

        assert removed_path not in selection.metadata
        assert removed_path not in selection.values

        data = selection.metadata.get(existing_path)
        assert data
        assert DataType.INT32 == data.data_type
        reader = selection.values.get(existing_path)
        assert reader
        assert reader.data_type == DataType.INT32

        data = selection.metadata.get(added_path)
        assert data
        assert DataType.STRING == data.data_type
        reader = selection.values.get(added_path)
        assert reader
        assert reader.data_type == DataType.STRING

    @pytest.mark.asyncio
    async def test__refresh_metadata_async__cached_values_for_deleted_tags_removed(
        self,
    ):
        path = "tag1"
        tags = [TagData(path, DataType.INT32)]
        selection = self.MockTagSelection(tags)
        selection.mock_read_tag_metadata_async.configure_mock(
            side_effect=[[TagData] * 0, tags]
        )
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        selection.refresh_values()
        await selection.refresh_metadata_async()
        await selection.refresh_metadata_async()

        assert (
            await selection.read_async(
                path, include_timestamp=True, include_aggregates=True
            )
            is None
        )

    def test__refresh_values__values_updated(self):
        value_path = "tag1"
        no_value_path = "tag2"
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        selection = self.MockTagSelection(
            [
                TagData(value_path, DataType.INT32),
                TagData(no_value_path, DataType.DATE_TIME),
            ]
        )
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[
                SerializedTagWithAggregates(
                    value_path, DataType.INT32, "5", timestamp, 3, "4", "9", 6.0
                )
            ],
        )

        selection.refresh_values()
        value = selection.read(
            value_path, include_timestamp=True, include_aggregates=True
        )

        assert value is not None
        assert DataType.INT32 == value.data_type
        assert 5 == value.value
        assert timestamp == value.timestamp
        assert 3 == value.count
        assert 4 == value.min
        assert 9 == value.max
        assert 6.0 == value.mean
        assert (
            selection.read(
                no_value_path, include_timestamp=True, include_aggregates=True
            )
            is None
        )

    def test__refresh_values__metadata_and_readers_updated_when_type_changes(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.BOOLEAN)])
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        original_reader = selection.values.get(path)
        assert original_reader
        assert original_reader.data_type == DataType.BOOLEAN
        selection.refresh_values()

        tag = selection.metadata.get(path)
        assert tag
        assert DataType.INT32 == tag.data_type
        new_reader = selection.values.get(path)
        assert new_reader
        assert new_reader.data_type == DataType.INT32

    def test__refresh_values__metadata_and_reader_added_for_new_tags(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        selection.refresh_values()

        tag = selection.metadata.get(path)
        assert tag
        assert DataType.INT32 == tag.data_type
        new_reader = selection.values.get(path)
        assert new_reader
        assert new_reader.data_type == DataType.INT32

    def test__refresh_values__deleted_tags_removed_from_cache(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.INT32)])
        selection.mock_read_tag_values.configure_mock(
            side_effect=[
                [SerializedTagWithAggregates(path, DataType.INT32, "5")],
                [SerializedTagWithAggregates] * 0,
            ]
        )

        selection.refresh_values()
        selection.refresh_values()

        assert (
            selection.read(path, include_timestamp=True, include_aggregates=True)
            is None
        )

    @pytest.mark.asyncio
    async def test__refresh_values_async__values_updated(self):
        value_path = "tag1"
        no_value_path = "tag2"
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        selection = self.MockTagSelection(
            [
                TagData(value_path, DataType.INT32),
                TagData(no_value_path, DataType.DATE_TIME),
            ]
        )
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=None,
            return_value=[
                SerializedTagWithAggregates(
                    value_path, DataType.INT32, "5", timestamp, 3, "4", "9", 6.0
                )
            ],
        )

        await selection.refresh_values_async()
        value = await selection.read_async(
            value_path, include_timestamp=True, include_aggregates=True
        )

        assert value is not None
        assert DataType.INT32 == value.data_type
        assert 5 == value.value
        assert timestamp == value.timestamp
        assert 3 == value.count
        assert 4 == value.min
        assert 9 == value.max
        assert 6.0 == value.mean
        assert (
            await selection.read_async(
                no_value_path, include_timestamp=True, include_aggregates=True
            )
            is None
        )

    @pytest.mark.asyncio
    async def test__refresh_values_async__metadata_and_readers_updated_when_type_changed(
        self,
    ):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.BOOLEAN)])
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        original_reader = selection.values.get(path)
        assert original_reader
        assert original_reader.data_type == DataType.BOOLEAN

        await selection.refresh_values_async()

        tag = selection.metadata.get(path)
        assert tag
        assert DataType.INT32 == tag.data_type
        new_reader = selection.values.get(path)
        assert new_reader
        assert new_reader.data_type == DataType.INT32

    @pytest.mark.asyncio
    async def test__refresh_values_async__metadata_and_reader_added_for_new_tags(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        await selection.refresh_values_async()

        tag = selection.metadata.get(path)
        assert tag
        assert DataType.INT32 == tag.data_type
        new_reader = selection.values.get(path)
        assert new_reader
        assert new_reader.data_type == DataType.INT32

    @pytest.mark.asyncio
    async def test__refresh_values_async__deleted_tags_removed_from_cache(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.INT32)])
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=[
                [SerializedTagWithAggregates(path, DataType.INT32, "5")],
                [SerializedTagWithAggregates] * 0,
            ]
        )

        await selection.refresh_values_async()
        await selection.refresh_values_async()

        assert (
            await selection.read_async(
                path, include_timestamp=True, include_aggregates=True
            )
            is None
        )

    def test__invalid_tags__remove_tags_by_metadata__raises_without_making_changes(
        self,
    ):
        selection = self.MockTagSelection([TagData] * 0)
        with pytest.raises(ValueError):
            selection.remove_tags(None)
        with pytest.raises(ValueError):
            selection.remove_tags([TagData("tag"), None])
        with pytest.raises(ValueError):
            selection.remove_tags([TagData("tag"), TagData("")])
        # The strict mock will assert that _on_paths_changed was never called.

    def test__remove_tags_by_metadata__paths_updated(self):
        path1 = "tag1"
        path2 = "tag2"
        selection = self.MockTagSelection(
            [TagData(path1, DataType.BOOLEAN), TagData(path2, DataType.DATE_TIME)]
        )
        selection.mock_on_paths_changed.configure_mock(side_effect=None)

        selection.remove_tags([TagData(path1)])

        assert [path2] == list(selection.paths)
        selection.mock_on_paths_changed.assert_called_once_with()

    def test__invalid_paths__remove_tags_by_path__raises_without_making_changes(self):
        selection = self.MockTagSelection([TagData] * 0)
        with pytest.raises(ValueError):
            selection.remove_tags(None)
        with pytest.raises(ValueError):
            selection.remove_tags(["tag", None])
        with pytest.raises(ValueError):
            selection.remove_tags(["tag", ""])
        # The strict mock will assert that _on_paths_changed was never called.

    def test__remove_tags_by_path__paths_updated(self):
        path1 = "tag1"
        path2 = "tag2"
        selection = self.MockTagSelection(
            [TagData(path1, DataType.BOOLEAN), TagData(path2, DataType.DATE_TIME)]
        )
        selection.mock_on_paths_changed.configure_mock(side_effect=None)

        selection.remove_tags([path1])

        assert [path2] == list(selection.paths)
        selection.mock_on_paths_changed.assert_called_once_with()

    def test__reset_aggregates__reset_aggregates_internal_called(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_reset_aggregates_internal.configure_mock(side_effect=None)
        selection.reset_aggregates()
        selection.mock_reset_aggregates_internal.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__reset_aggregates_async__reset_aggregates_internal_called(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_reset_aggregates_internal_async.configure_mock(side_effect=None)
        await selection.reset_aggregates_async()
        selection.mock_reset_aggregates_internal_async.assert_called_once_with()

    def test__close__close_internal_called(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_close_internal.configure_mock(side_effect=None)

        selection.close()
        selection.mock_close_internal.assert_called_once_with()

    def test__new_selection__read__values_refreshed(self):
        value_path = "tag1"
        no_value_path = "tag2"
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        selection = self.MockTagSelection(
            [
                TagData(value_path, DataType.INT32),
                TagData(no_value_path, DataType.DATE_TIME),
            ]
        )
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[
                SerializedTagWithAggregates(
                    value_path, DataType.INT32, "5", timestamp, 3, "4", "9", 6.0
                )
            ],
        )

        value = selection.read(
            value_path, include_timestamp=True, include_aggregates=True
        )

        assert value is not None
        assert DataType.INT32 == value.data_type
        assert 5 == value.value
        assert timestamp == value.timestamp
        assert 3 == value.count
        assert 4 == value.min
        assert 9 == value.max
        assert 6.0 == value.mean
        assert (
            selection.read(
                no_value_path, include_timestamp=True, include_aggregates=True
            )
            is None
        )
        selection.mock_read_tag_values.assert_called_once_with()

    def test__values_cached__read__cached_values_used(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.INT32)])
        selection.mock_read_tag_values.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        assert selection._read(
            path, include_timestamp=True, include_aggregates=True
        ) is selection._read(path, include_timestamp=True, include_aggregates=True)
        assert (
            selection._read(path, include_timestamp=True, include_aggregates=True)
            is not None
        )
        selection.mock_read_tag_values.assert_called_once_with()

    def test__tag_has_no_value__read__returns_null(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.INT32)])
        selection.mock_read_tag_values.configure_mock(
            side_effect=None, return_value=[SerializedTagWithAggregates] * 0
        )

        assert (
            selection.read(path, include_timestamp=True, include_aggregates=True)
            is None
        )
        selection.mock_read_tag_values.assert_called_once_with()

    def test__tags_not_in_selection__read__raises(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_read_tag_values.configure_mock(
            side_effect=None, return_value=[SerializedTagWithAggregates] * 0
        )
        with pytest.raises(ValueError):
            selection.read(None, include_timestamp=True, include_aggregates=True)
        with pytest.raises(ValueError):
            selection.read("tag", include_timestamp=True, include_aggregates=True)

    @pytest.mark.asyncio
    async def test__new_selection__read_async__values_refreshed(self):
        value_path = "tag1"
        no_value_path = "tag2"
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        selection = self.MockTagSelection(
            [
                TagData(value_path, DataType.INT32),
                TagData(no_value_path, DataType.DATE_TIME),
            ]
        )
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=None,
            return_value=[
                SerializedTagWithAggregates(
                    value_path, DataType.INT32, "5", timestamp, 3, "4", "9", 6.0
                )
            ],
        )

        value = await selection.read_async(
            value_path, include_timestamp=True, include_aggregates=True
        )

        assert value is not None
        assert DataType.INT32 == value.data_type
        assert 5 == value.value
        assert timestamp == value.timestamp
        assert 3 == value.count
        assert 4 == value.min
        assert 9 == value.max
        assert 6.0 == value.mean
        assert (
            await selection.read_async(
                no_value_path, include_timestamp=True, include_aggregates=True
            )
            is None
        )
        selection.mock_read_tag_values_async.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__values_cached__read_async__cached_values_used(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.INT32)])
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=None,
            return_value=[SerializedTagWithAggregates(path, DataType.INT32, "5")],
        )

        assert await selection._read_async(
            path, True, True
        ) is await selection._read_async(
            path, include_timestamp=True, include_aggregates=True
        )
        assert (
            await selection._read_async(
                path, include_timestamp=True, include_aggregates=True
            )
            is not None
        )
        selection.mock_read_tag_values_async.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__tag_has_no_value__read_async__returns_null(self):
        path = "tag1"
        selection = self.MockTagSelection([TagData(path, DataType.INT32)])
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=None, return_value=[SerializedTagWithAggregates] * 0
        )

        assert (
            await selection.read_async(
                path, include_timestamp=True, include_aggregates=True
            )
            is None
        )
        selection.mock_read_tag_values_async.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__tags_not_in_selection__read_async__raises(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_read_tag_values_async.configure_mock(
            side_effect=None, return_value=[SerializedTagWithAggregates] * 0
        )
        with pytest.raises(ValueError):
            await selection.read_async(
                None, include_timestamp=True, include_aggregates=True
            )
        with pytest.raises(ValueError):
            await selection.read_async(
                "tag", include_timestamp=True, include_aggregates=True
            )

    @pytest.mark.asyncio
    async def test__after_close__method_called__raises(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_close_internal.configure_mock(side_effect=None)
        selection.close()

        with pytest.raises(ReferenceError):
            selection.add_tags([TagData("tag")])
        with pytest.raises(ReferenceError):
            selection.clear_tags()
        selection.close()
        await selection.close_async()
        with pytest.raises(ReferenceError):
            selection.create_subscription()
        with pytest.raises(ReferenceError):
            selection.create_subscription(update_interval=datetime.timedelta(seconds=1))
        with pytest.raises(ReferenceError):
            await selection.create_subscription_async()
        with pytest.raises(ReferenceError):
            await selection.create_subscription_async(
                update_interval=datetime.timedelta(seconds=1)
            )
        with pytest.raises(ReferenceError):
            selection.delete_tags_from_server()
        with pytest.raises(ReferenceError):
            await selection.delete_tags_from_server_async()
        with pytest.raises(ReferenceError):
            selection.open_tags(["tag"])
        with pytest.raises(ReferenceError):
            selection.refresh()
        with pytest.raises(ReferenceError):
            await selection.refresh_async()
        with pytest.raises(ReferenceError):
            selection.refresh_metadata()
        with pytest.raises(ReferenceError):
            await selection.refresh_metadata_async()
        with pytest.raises(ReferenceError):
            selection.refresh_values()
        with pytest.raises(ReferenceError):
            await selection.refresh_values_async()
        with pytest.raises(ReferenceError):
            selection.remove_tags([TagData("tag")])
        with pytest.raises(ReferenceError):
            selection.remove_tags(["tag"])
        with pytest.raises(ReferenceError):
            selection.reset_aggregates()
        with pytest.raises(ReferenceError):
            await selection.reset_aggregates_async()
        selection.close()
        with pytest.raises(ReferenceError):
            selection.read("tag", include_timestamp=True, include_aggregates=True)
        with pytest.raises(ReferenceError):
            await selection.read_async(
                "tag", include_timestamp=True, include_aggregates=True
            )

        selection.mock_close_internal.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__selection_context_exited__method_called__raises(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_close_internal.configure_mock(side_effect=None)
        with selection:
            pass

        with pytest.raises(ReferenceError):
            selection.add_tags([TagData("tag")])
        with pytest.raises(ReferenceError):
            selection.clear_tags()
        selection.close()
        await selection.close_async()
        with pytest.raises(ReferenceError):
            selection.create_subscription()
        with pytest.raises(ReferenceError):
            selection.create_subscription(update_interval=datetime.timedelta(seconds=1))
        with pytest.raises(ReferenceError):
            await selection.create_subscription_async()
        with pytest.raises(ReferenceError):
            await selection.create_subscription_async(
                update_interval=datetime.timedelta(seconds=1)
            )
        with pytest.raises(ReferenceError):
            selection.delete_tags_from_server()
        with pytest.raises(ReferenceError):
            await selection.delete_tags_from_server_async()
        with pytest.raises(ReferenceError):
            selection.open_tags(["tag"])
        with pytest.raises(ReferenceError):
            selection.refresh()
        with pytest.raises(ReferenceError):
            await selection.refresh_async()
        with pytest.raises(ReferenceError):
            selection.refresh_metadata()
        with pytest.raises(ReferenceError):
            await selection.refresh_metadata_async()
        with pytest.raises(ReferenceError):
            selection.refresh_values()
        with pytest.raises(ReferenceError):
            await selection.refresh_values_async()
        with pytest.raises(ReferenceError):
            selection.remove_tags([TagData("tag")])
        with pytest.raises(ReferenceError):
            selection.remove_tags(["tag"])
        with pytest.raises(ReferenceError):
            selection.reset_aggregates()
        with pytest.raises(ReferenceError):
            await selection.reset_aggregates_async()
        selection.close()
        with pytest.raises(ReferenceError):
            selection.read("tag", include_timestamp=True, include_aggregates=True)
        with pytest.raises(ReferenceError):
            await selection.read_async(
                "tag", include_timestamp=True, include_aggregates=True
            )

        selection.mock_close_internal.assert_called_once_with()

    @pytest.mark.asyncio
    async def test__after_close_async__method_called__raises(self):
        selection = self.MockTagSelection([TagData] * 0)
        selection.mock_close_internal_async.configure_mock(side_effect=None)
        await selection.close_async()

        with pytest.raises(ReferenceError):
            selection.add_tags([TagData("tag")])
        with pytest.raises(ReferenceError):
            selection.clear_tags()
        selection.close()
        await selection.close_async()
        with pytest.raises(ReferenceError):
            selection.create_subscription()
        with pytest.raises(ReferenceError):
            selection.create_subscription(update_interval=datetime.timedelta(seconds=1))
        with pytest.raises(ReferenceError):
            await selection.create_subscription_async()
        with pytest.raises(ReferenceError):
            await selection.create_subscription_async(
                update_interval=datetime.timedelta(seconds=1)
            )
        with pytest.raises(ReferenceError):
            selection.delete_tags_from_server()
        with pytest.raises(ReferenceError):
            await selection.delete_tags_from_server_async()
        with pytest.raises(ReferenceError):
            selection.open_tags(["tag"])
        with pytest.raises(ReferenceError):
            selection.refresh()
        with pytest.raises(ReferenceError):
            await selection.refresh_async()
        with pytest.raises(ReferenceError):
            selection.refresh_metadata()
        with pytest.raises(ReferenceError):
            await selection.refresh_metadata_async()
        with pytest.raises(ReferenceError):
            selection.refresh_values()
        with pytest.raises(ReferenceError):
            await selection.refresh_values_async()
        with pytest.raises(ReferenceError):
            selection.remove_tags([TagData("tag")])
        with pytest.raises(ReferenceError):
            selection.remove_tags(["tag"])
        with pytest.raises(ReferenceError):
            selection.reset_aggregates()
        with pytest.raises(ReferenceError):
            await selection.reset_aggregates_async()
        selection.close()
        with pytest.raises(ReferenceError):
            selection.read("tag", include_timestamp=True, include_aggregates=True)
        with pytest.raises(ReferenceError):
            await selection.read_async(
                "tag", include_timestamp=True, include_aggregates=True
            )

        selection.mock_close_internal_async.assert_called_once_with()

    class MockTagSelection(TagSelection):
        def __init__(self, tags, paths=None):
            super().__init__(tags, paths)

            self.mock_buffer_value = Mock(side_effect=NotImplementedError)
            self.mock_close_internal = Mock(return_value=None)
            self.mock_close_internal_async = Mock(side_effect=NotImplementedError)
            self.mock_create_subscription_internal = Mock(
                side_effect=NotImplementedError
            )
            self.mock_create_subscription_internal_async = Mock(
                side_effect=NotImplementedError
            )
            self.mock_delete_tags_from_server_internal = Mock(
                side_effect=NotImplementedError
            )
            self.mock_delete_tags_from_server_internal_async = Mock(
                side_effect=NotImplementedError
            )
            self.mock_on_paths_changed = Mock(wraps=super()._on_paths_changed)
            self.mock_read_tag_metadata = Mock(side_effect=NotImplementedError)
            self.mock_read_tag_metadata_and_values = Mock(
                side_effect=NotImplementedError
            )
            self.mock_read_tag_metadata_and_values_async = Mock(
                side_effect=NotImplementedError
            )
            self.mock_read_tag_metadata_async = Mock(side_effect=NotImplementedError)
            self.mock_read_tag_values = Mock(side_effect=NotImplementedError)
            self.mock_read_tag_values_async = Mock(side_effect=NotImplementedError)
            self.mock_reset_aggregates_internal = Mock(side_effect=NotImplementedError)
            self.mock_reset_aggregates_internal_async = Mock(
                side_effect=NotImplementedError
            )

        def _close_internal(self, *args, **kwargs):
            return self.mock_close_internal(*args, **kwargs)

        async def _close_internal_async(self, *args, **kwargs):
            return self.mock_close_internal_async(*args, **kwargs)

        def _create_subscription_internal(self, *args, **kwargs):
            return self.mock_create_subscription_internal(*args, **kwargs)

        async def _create_subscription_internal_async(self, *args, **kwargs):
            return self.mock_create_subscription_internal_async(*args, **kwargs)

        def _delete_tags_from_server_internal(self, *args, **kwargs):
            return self.mock_delete_tags_from_server_internal(*args, **kwargs)

        async def _delete_tags_from_server_internal_async(self, *args, **kwargs):
            return self.mock_delete_tags_from_server_internal_async(*args, **kwargs)

        def _on_paths_changed(self, *args, **kwargs):
            return self.mock_on_paths_changed(*args, **kwargs)

        def _read_tag_metadata(self, *args, **kwargs):
            return self.mock_read_tag_metadata(*args, **kwargs)

        def _read_tag_metadata_and_values(self, *args, **kwargs):
            return self.mock_read_tag_metadata_and_values(*args, **kwargs)

        async def _read_tag_metadata_and_values_async(self, *args, **kwargs):
            return self.mock_read_tag_metadata_and_values_async(*args, **kwargs)

        async def _read_tag_metadata_async(self, *args, **kwargs):
            return self.mock_read_tag_metadata_async(*args, **kwargs)

        def _read_tag_values(self, *args, **kwargs):
            return self.mock_read_tag_values(*args, **kwargs)

        async def _read_tag_values_async(self, *args, **kwargs):
            return self.mock_read_tag_values_async(*args, **kwargs)

        def _reset_aggregates_internal(self, *args, **kwargs):
            return self.mock_reset_aggregates_internal(*args, **kwargs)

        async def _reset_aggregates_internal_async(self, *args, **kwargs):
            return self.mock_reset_aggregates_internal_async(*args, **kwargs)
