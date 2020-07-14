import pytest  # type: ignore
from systemlink.clients.core import ApiException
from systemlink.clients.tag import DataType, TagData, TagQueryResultCollection


class TestTagQueryResultCollectionTests:
    class MockTagQueryResultCollection(TagQueryResultCollection):
        def __init__(self, first_page, total_count, skip):
            super().__init__(first_page, total_count, skip)
            self._setup_called = False
            self._next_total_count = None
            self._next_page = []
            self._next_throw = None
            self._calls = []

        def setup(self, next_page, new_total_count=None):
            assert (
                not self._setup_called
            ), "setup called without previous call to _query_page"
            self._setup_called = True
            if isinstance(next_page, Exception):
                self._next_throw = next_page
                self._next_page = None
            else:
                self._next_page = next_page
                self._next_throw = None
            self._next_total_count = new_total_count

        def verify(self, expected_skips):
            assert expected_skips == self._calls

        def _query_page(self, skip):
            assert self._setup_called, "_query_page called without call to setup"
            self._setup_called = False
            self._calls.append(skip)

            if self._next_throw is not None:
                raise self._next_throw

            if self._next_total_count is not None:
                self._total_count = self._next_total_count

            return self._next_page

        @property
        def total_count(self):
            return self._total_count

    def test__constructed__has_first_page_of_data(self):
        data = [
            TagData("tag1", DataType.BOOLEAN),
            TagData("tag2", DataType.DATE_TIME),
            TagData("tag3", DataType.DOUBLE),
        ]

        uut = self.MockTagQueryResultCollection(data, len(data), 0)

        itr = iter(uut)
        assert data == next(itr)
        assert len(data) == uut.total_count

    def test__iterating__second_page_queried(self):
        first_page = [
            TagData("tag1", DataType.BOOLEAN),
            TagData("tag2", DataType.DATE_TIME),
        ]

        second_page = [TagData("tag3", DataType.DOUBLE)]

        uut = self.MockTagQueryResultCollection(
            first_page, len(first_page) + len(second_page), 0
        )
        uut.setup(second_page)

        itr = iter(uut)
        next(itr)
        page = next(itr)
        assert len(first_page) + len(second_page) == uut.total_count
        assert second_page == page
        uut.verify([len(first_page)])

    def test__iterating__skip_is_respected(self):
        tag1 = TagData("tag1", DataType.BOOLEAN)
        tag2 = TagData("tag2", DataType.DATE_TIME)
        tag3 = TagData("tag3", DataType.DOUBLE)
        page1 = [tag1] * 2
        page2 = [tag2] * 5
        page3 = [tag3] * 1
        initial_skip = 1
        total_count = initial_skip + len(page1) + len(page2) + len(page3)

        uut = self.MockTagQueryResultCollection(page1, total_count, initial_skip)
        itr = iter(uut)

        next(itr)
        uut.setup(page2)
        next(itr)
        uut.setup(page3)
        next(itr)

        uut.verify([initial_skip + len(page1), initial_skip + len(page1) + len(page2)])

    def test__iterating__stops_when_done(self):
        tag = TagData("tag1", DataType.BOOLEAN)
        uut = self.MockTagQueryResultCollection([tag], 1, 0)

        assert 1 == uut.total_count

        itr = iter(uut)

        page = next(itr)
        assert len(page) == 1
        assert tag is page[0]

        with pytest.raises(StopIteration):
            next(itr)

    def test__page_count_changes__iterating__stops_early(self):
        tag = TagData("tag1", DataType.BOOLEAN)
        initial_total_count = 2
        uut = self.MockTagQueryResultCollection([tag], initial_total_count, 0)
        uut.setup(None, new_total_count=1)

        itr = iter(uut)
        next(itr)
        # according to initial_total_count, there should be more data, but there's not
        # - and that should be okay, but iterating should not produce any more results
        with pytest.raises(StopIteration):
            next(itr)

        uut.verify([1])

    def test__total_count_changes__iterating__total_count_updated(self):
        tag1 = TagData("tag1", DataType.BOOLEAN)
        tag2 = TagData("tag2", DataType.DATE_TIME)
        uut = self.MockTagQueryResultCollection([tag1], 3, 0)

        itr = iter(uut)

        page = next(itr)
        assert 3 == uut.total_count
        uut.setup([tag2], new_total_count=2)

        page = next(itr)
        assert 2 == uut.total_count
        assert 1 == len(page)
        assert tag2 is page[0]
        uut.verify([1])

        with pytest.raises(StopIteration):
            next(itr)
        assert 2 == uut.total_count
        uut.verify([1])  # still only one query has happened, due to new total_count

    def test__restart_iter__page_is_queried_with_initial_skip(self):
        initial_skip = 1
        tag2 = TagData("tag2", DataType.DATE_TIME)
        uut = self.MockTagQueryResultCollection([tag2], 3, initial_skip)

        itr = iter(uut)
        next(itr)

        tag2b = TagData("tag2b", DataType.DATE_TIME)
        uut.setup([tag2b], new_total_count=2)

        itr = iter(uut)

        page = next(itr)
        assert 2 == uut.total_count
        assert 1 == len(page)
        assert tag2b is page[0]

        with pytest.raises(StopIteration):
            next(itr)

        uut.verify([initial_skip])

    def test__no_results__constructed__iteration_is_empty(self):
        uut = self.MockTagQueryResultCollection(None, 0, 0)
        assert 0 == uut.total_count

        itr = iter(uut)
        with pytest.raises(StopIteration):
            next(itr)

    def test__server_data_removed_after_query__restart_iter__query_has_no_results(self):
        tag = TagData("tag", DataType.INT32)
        uut = self.MockTagQueryResultCollection([tag], 1, 0)

        itr = iter(uut)
        next(itr)
        assert 1 == uut.total_count

        uut.setup(None, new_total_count=0)

        itr = iter(uut)
        with pytest.raises(StopIteration):
            next(itr)
        assert 0 == uut.total_count
        uut.verify([0])

    def test__server_data_added_after_empty_query__restart_iter__query_has_results(
        self,
    ):
        tags = [TagData("tag", DataType.INT32)]
        uut = self.MockTagQueryResultCollection(None, 0, 0)

        itr = iter(uut)
        with pytest.raises(StopIteration):
            next(itr)

        uut.setup(tags, new_total_count=1)

        itr = iter(uut)

        page = next(itr)
        assert 1 == uut.total_count
        assert tags == page

        with pytest.raises(StopIteration):
            next(itr)

        uut.verify([0])

    def test__server_error__iterating__client_sees_error_but_can_restart(self):
        exception_to_throw = ApiException()
        initial_tags = [TagData("tag", DataType.INT32)]
        next_page = [TagData("tag2", DataType.STRING)]
        uut = self.MockTagQueryResultCollection(initial_tags, 2, 0)

        itr = iter(uut)
        next(itr)
        uut.setup(exception_to_throw)

        with pytest.raises(ApiException):
            next(itr)

        # Try again after error -- let it work this time
        uut.setup(next_page)
        itr = iter(uut)
        page = next(itr)
        assert next_page == page

        uut.verify([1, 0])

    def test__server_error__restart_iter__client_sees_error_but_can_retry(self):
        exception_to_throw = ApiException()
        initial_tags = [TagData("tag", DataType.INT32)]
        first_page = [TagData("tag2", DataType.STRING)]
        uut = self.MockTagQueryResultCollection(initial_tags, 1, 0)

        itr = iter(uut)
        next(itr)

        uut.setup(exception_to_throw)
        itr = iter(uut)
        with pytest.raises(ApiException):
            next(itr)

        # Try again after error -- let it work this time
        uut.setup(first_page)
        itr = iter(uut)
        page = next(itr)
        assert first_page == page
        with pytest.raises(StopIteration):
            next(itr)

        uut.verify([0, 0])
