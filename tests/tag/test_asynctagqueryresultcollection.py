import asyncio

import pytest  # type: ignore
from systemlink.clients.core import ApiException
from systemlink.clients.tag import AsyncTagQueryResultCollection, DataType, TagData


class TestAsyncTagQueryResultCollection:
    class MockAsyncTagQueryResultCollection(AsyncTagQueryResultCollection):
        def __init__(self, first_page, total_count, skip):
            super().__init__(first_page, total_count, skip)
            self._setup_called = False
            self._next_total_count = None
            self._next_page = []
            self._next_throw = None
            self._calls = []

        def setup(
            self, *, next_page=None, new_total_count=None, exception_to_throw=None
        ):
            assert (
                not self._setup_called
            ), "setup called without previous call to _query_page_async"
            self._setup_called = True
            self._next_page = next_page
            self._next_total_count = new_total_count
            self._next_throw = exception_to_throw

        def verify(self, expected_skips):
            assert expected_skips == self._calls

        def _query_page_async(self, skip):
            assert self._setup_called, "_query_page_async called without call to setup"
            self._setup_called = False
            self._calls.append(skip)

            if self._next_throw is not None:
                f = asyncio.get_event_loop().create_future()
                f.set_exception(self._next_throw)
                return f

            if self._next_total_count is not None:
                self._total_count = self._next_total_count

            f = asyncio.get_event_loop().create_future()
            f.set_result(self._next_page)
            return f

    def test__constructed__has_first_page_of_data(self):
        data = [
            TagData("tag1", DataType.BOOLEAN),
            TagData("tag2", DataType.DATE_TIME),
            TagData("tag3", DataType.DOUBLE),
        ]

        uut = self.MockAsyncTagQueryResultCollection(data, len(data), 0)

        assert data == list(uut.current_page)
        assert len(data) == uut.total_count

    @pytest.mark.asyncio
    async def test__move_next_page__current_page_queried_and_updated(self):
        first_page = [
            TagData("tag1", DataType.BOOLEAN),
            TagData("tag2", DataType.DATE_TIME),
        ]

        second_page = [TagData("tag3", DataType.DOUBLE)]

        uut = self.MockAsyncTagQueryResultCollection(
            first_page, len(first_page) + len(second_page), 0
        )
        uut.setup(next_page=second_page)

        await uut.move_next_page_async()
        assert len(first_page) + len(second_page) == uut.total_count
        assert second_page == uut.current_page
        uut.verify([len(first_page)])

    @pytest.mark.asyncio
    async def test__move_next_page__skip_is_respected(self):
        page1 = 2
        page2 = 5
        page3 = 1
        initial_skip = 1
        total_count = initial_skip + page1 + page2 + page3

        tag1 = TagData("tag1", DataType.BOOLEAN)
        tag2 = TagData("tag2", DataType.DATE_TIME)
        tag3 = TagData("tag3", DataType.DOUBLE)

        uut = self.MockAsyncTagQueryResultCollection(
            [tag1] * page1, total_count, initial_skip
        )
        uut.setup(next_page=[tag2] * page2)

        await uut.move_next_page_async()
        uut.setup(next_page=[tag3] * page3)
        await uut.move_next_page_async()

        uut.verify([initial_skip + page1, initial_skip + page1 + page2])

    @pytest.mark.asyncio
    async def test__on_last_page__move_next_page__current_page_set_to_null(self):
        tag = TagData("tag1", DataType.BOOLEAN)
        uut = self.MockAsyncTagQueryResultCollection([tag], 1, 0)

        assert 1 == uut.total_count
        assert 1 == len(uut.current_page)
        assert tag is uut.current_page[0]

        await uut.move_next_page_async()
        assert 1 == uut.total_count
        assert uut.current_page is None

        await uut.move_next_page_async()
        assert 1 == uut.total_count
        assert uut.current_page is None

    @pytest.mark.asyncio
    async def test__page_count_changes__move_next_page__current_page_set_to_null(self):
        tag = TagData("tag1", DataType.BOOLEAN)
        initial_total_count = 2
        uut = self.MockAsyncTagQueryResultCollection([tag], initial_total_count, 0)
        uut.setup(new_total_count=1)

        # according to initial_total_count, there should be more data, but there's not
        # - and that should be okay, and clear the current_page
        await uut.move_next_page_async()
        assert uut.current_page is None

        await uut.move_next_page_async()
        assert uut.current_page is None

        uut.verify([1])

    @pytest.mark.asyncio
    async def test__total_count_changes__move_next_page__total_count_updated(self):
        tag1 = TagData("tag1", DataType.BOOLEAN)
        tag2 = TagData("tag2", DataType.DATE_TIME)
        uut = self.MockAsyncTagQueryResultCollection([tag1], 3, 0)
        uut.setup(next_page=[tag2], new_total_count=2)

        assert 3 == uut.total_count
        await uut.move_next_page_async()
        assert 2 == uut.total_count
        assert 1 == len(uut.current_page)
        assert tag2 is uut.current_page[0]
        uut.verify([1])

        await uut.move_next_page_async()
        assert 2 == uut.total_count
        assert uut.current_page is None
        uut.verify([1])  # still only one query has happened, due to new total_count

    @pytest.mark.asyncio
    async def test__reset__page_is_queried_with_initial_skip(self):
        initial_skip = 1
        tag2 = TagData("tag2", DataType.DATE_TIME)
        uut = self.MockAsyncTagQueryResultCollection([tag2], 3, initial_skip)

        tag2b = TagData("tag2b", DataType.DATE_TIME)
        uut.setup(next_page=[tag2b], new_total_count=2)
        await uut.reset_async()

        assert 2 == uut.total_count
        assert 1 == len(uut.current_page)
        assert tag2b is uut.current_page[0]

        await uut.move_next_page_async()
        assert uut.current_page is None

        uut.verify([initial_skip])

    @pytest.mark.asyncio
    async def test__no_results__constructed__current_page_is_null(self):
        uut = self.MockAsyncTagQueryResultCollection(None, 0, 0)
        assert 0 == uut.total_count
        assert uut.current_page is None

        await uut.move_next_page_async()
        assert uut.current_page is None

    @pytest.mark.asyncio
    async def test__server_data_removed_after_query__reset__query_has_no_results(self):
        tag = TagData("tag", DataType.INT32)
        uut = self.MockAsyncTagQueryResultCollection([tag], 1, 0)
        assert 1 == uut.total_count
        assert uut.current_page is not None

        uut.setup(new_total_count=0)
        await uut.reset_async()
        assert 0 == uut.total_count
        assert uut.current_page is None

        await uut.move_next_page_async()
        assert uut.current_page is None

        uut.verify([0])

    @pytest.mark.asyncio
    async def test__server_data_added_after_empty_query__reset__query_has_results(self):
        tags = [TagData("tag", DataType.INT32)]
        uut = self.MockAsyncTagQueryResultCollection(None, 0, 0)
        uut.setup(next_page=tags, new_total_count=1)

        await uut.reset_async()
        assert 1 == uut.total_count
        assert tags == uut.current_page

        await uut.move_next_page_async()
        assert uut.current_page is None

        uut.verify([0])

    @pytest.mark.asyncio
    async def test__server_error__move_next_page__client_sees_error_but_can_continue(
        self,
    ):
        exception_to_throw = ApiException()
        initial_tags = [TagData("tag", DataType.INT32)]
        next_page = [TagData("tag2", DataType.STRING)]
        uut = self.MockAsyncTagQueryResultCollection(initial_tags, 2, 0)
        uut.setup(exception_to_throw=exception_to_throw)

        with pytest.raises(ApiException):
            await uut.move_next_page_async()
        # After the failure, the current_page should remain unchanged
        assert initial_tags == uut.current_page

        # Try again after error -- let it work this time
        uut.setup(next_page=next_page)
        await uut.move_next_page_async()
        assert next_page == uut.current_page

        uut.verify([1, 1])

    @pytest.mark.asyncio
    async def test__server_error__reset__client_sees_error_but_can_retry(self):
        exception_to_throw = ApiException()
        initial_tags = [TagData("tag", DataType.INT32)]
        first_page = [TagData("tag2", DataType.STRING)]
        uut = self.MockAsyncTagQueryResultCollection(initial_tags, 1, 0)
        uut.setup(exception_to_throw=exception_to_throw)

        # After the failure, the current_page should remain unchanged
        with pytest.raises(ApiException):
            await uut.reset_async()
        assert initial_tags == uut.current_page

        # Try again after error -- let it work this time
        uut.setup(next_page=first_page)
        await uut.reset_async()
        assert first_page == uut.current_page

        uut.verify([0, 0])
