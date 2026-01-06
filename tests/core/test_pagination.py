# -*- coding: utf-8 -*-
"""Tests for the pagination helper function."""

from typing import Any, List
from unittest.mock import MagicMock

import pytest
from nisystemlink.clients.core.helpers import paginate


class MockResponse:
    """Mock API response object for testing pagination."""

    def __init__(self, items: List[Any], continuation_token: str | None = None):
        self.items = items
        self.continuation_token = continuation_token


class MockResponseCustomFields:
    """Mock API response with custom field names."""

    def __init__(self, results: List[Any], continuation_token: str | None = None):
        self.results = results
        self.continuation_token = continuation_token


class TestPaginate:
    """Tests for the paginate helper function."""

    def test__paginate_single_page__yields_all_items(self):
        """Test pagination with a single page of results."""
        # Arrange
        items = [1, 2, 3, 4, 5]
        mock_fetch = MagicMock(return_value=MockResponse(items, None))

        # Act
        result = list(paginate(mock_fetch, "items"))

        # Assert
        assert result == items
        assert mock_fetch.call_count == 1
        mock_fetch.assert_called_with(continuation_token=None)

    def test__paginate_multiple_pages__yields_all_items_in_order(self):
        """Test pagination with multiple pages."""
        # Arrange
        page1_items = [1, 2, 3]
        page2_items = [4, 5, 6]
        page3_items = [7, 8, 9]

        mock_fetch = MagicMock(
            side_effect=[
                MockResponse(page1_items, "token1"),
                MockResponse(page2_items, "token2"),
                MockResponse(page3_items, None),
            ]
        )

        # Act
        result = list(paginate(mock_fetch, "items"))

        # Assert
        assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert mock_fetch.call_count == 3
        assert mock_fetch.call_args_list[0][1]["continuation_token"] is None
        assert mock_fetch.call_args_list[1][1]["continuation_token"] == "token1"
        assert mock_fetch.call_args_list[2][1]["continuation_token"] == "token2"

    def test__paginate_with_custom_items_field__yields_all_items(self):
        """Test pagination with custom items field name."""
        # Arrange
        page1_results = ["a", "b"]
        page2_results = ["c", "d"]

        mock_fetch = MagicMock(
            side_effect=[
                MockResponseCustomFields(page1_results, "next1"),
                MockResponseCustomFields(page2_results, None),
            ]
        )

        # Act
        result = list(paginate(mock_fetch, items_field="results"))

        # Assert
        assert result == ["a", "b", "c", "d"]
        assert mock_fetch.call_count == 2

    def test__paginate_with_additional_kwargs__passes_kwargs_to_fetch(self):
        """Test that additional keyword arguments are passed to the fetch function."""
        # Arrange
        items = [1, 2, 3]
        mock_fetch = MagicMock(return_value=MockResponse(items, None))

        # Act
        result = list(
            paginate(
                mock_fetch, "items", take=10, filter="status==PASSED", return_count=True
            )
        )

        # Assert
        assert result == items
        mock_fetch.assert_called_once_with(
            continuation_token=None, take=10, filter="status==PASSED", return_count=True
        )

    def test__paginate_empty_results__returns_empty(self):
        """Test pagination with no results."""
        # Arrange
        mock_fetch = MagicMock(return_value=MockResponse([], None))

        # Act
        result = list(paginate(mock_fetch, "items"))

        # Assert
        assert result == []
        assert mock_fetch.call_count == 1

    def test__paginate_empty_page_in_middle__yields_only_non_empty_pages(self):
        """Test pagination when a middle page is empty."""
        # Arrange
        page1_items = [1, 2, 3]
        page2_items = []
        page3_items = [4, 5]

        mock_fetch = MagicMock(
            side_effect=[
                MockResponse(page1_items, "token1"),
                MockResponse(page2_items, "token2"),
                MockResponse(page3_items, None),
            ]
        )

        # Act
        result = list(paginate(mock_fetch, "items"))

        # Assert
        assert result == [1, 2, 3, 4, 5]
        assert mock_fetch.call_count == 3

    def test__paginate_generator__can_be_used_in_for_loop(self):
        """Test that paginate works as expected in a for loop."""
        # Arrange
        page1_items = [1, 2]
        page2_items = [3, 4]
        mock_fetch = MagicMock(
            side_effect=[
                MockResponse(page1_items, "token1"),
                MockResponse(page2_items, None),
            ]
        )

        # Act
        collected = []
        for item in paginate(mock_fetch, "items"):
            collected.append(item * 2)

        # Assert
        assert collected == [2, 4, 6, 8]

    def test__paginate_lazy_evaluation__only_fetches_as_needed(self):
        """Test that pagination is lazy and doesn't fetch all pages immediately."""
        # Arrange
        page1_items = [1, 2, 3]
        page2_items = [4, 5, 6]
        mock_fetch = MagicMock(
            side_effect=[
                MockResponse(page1_items, "token1"),
                MockResponse(page2_items, None),
            ]
        )

        # Act
        gen = paginate(mock_fetch, "items")
        assert mock_fetch.call_count == 0  # Nothing called yet

        first_item = next(gen)
        assert first_item == 1
        assert mock_fetch.call_count == 1  # First page fetched

        # Consume rest of first page
        next(gen)  # 2
        next(gen)  # 3

        # First page exhausted, but second page not yet fetched
        assert mock_fetch.call_count == 1

        # Fetch first item of second page
        fourth_item = next(gen)
        assert fourth_item == 4
        assert mock_fetch.call_count == 2  # Second page fetched

    def test__paginate_with_kwargs_persisted_across_pages__kwargs_used_on_all_calls(
        self,
    ):
        """Test that kwargs are passed to all fetch function calls."""
        # Arrange
        mock_fetch = MagicMock(
            side_effect=[
                MockResponse([1, 2], "token1"),
                MockResponse([3, 4], None),
            ]
        )

        # Act
        list(paginate(mock_fetch, "items", take=100, filter="active==true"))

        # Assert
        for call in mock_fetch.call_args_list:
            assert call[1]["take"] == 100
            assert call[1]["filter"] == "active==true"

    def test__paginate_missing_items_field__yields_nothing(self):
        """Test pagination when the items field doesn't exist on the response."""
        # Arrange
        mock_response = MockResponse([], None)
        # Remove the items field
        delattr(mock_response, "items")
        mock_fetch = MagicMock(return_value=mock_response)

        # Act
        result = list(paginate(mock_fetch, "items"))

        # Assert
        assert result == []
        assert mock_fetch.call_count == 1

    def test__paginate_continuation_token_unchanged__raises_runtime_error(self):
        """Test that an error is raised if the continuation token doesn't change."""
        # Arrange
        # First call returns token1, second call returns token1 again (infinite loop)
        mock_fetch = MagicMock(
            side_effect=[
                MockResponse([1, 2], "token1"),
                MockResponse([3, 4], "token1"),  # Same token - should raise error
            ]
        )

        # Act & Assert
        with pytest.raises(RuntimeError, match="Continuation token did not change"):
            list(paginate(mock_fetch, "items"))

        # Should have made 2 calls before detecting the issue
        assert mock_fetch.call_count == 2
