# -*- coding: utf-8 -*-

"""Tests for read_minion_id helper function."""

from pathlib import Path
from unittest import mock

from nisystemlink.clients.core.helpers._minion_id import read_minion_id


class TestReadMinionId:
    """Test cases for read_minion_id function."""

    def _setup_mock_path(self, mock_path_constants, exists=True):
        """Helper to set up the mock path structure."""
        mock_minion_id_path = mock.Mock(spec=Path)
        mock_minion_id_path.exists.return_value = exists

        # Set up the path chain: salt_data_directory / "conf" / "minion_id"
        mock_conf_path = mock.Mock(spec=Path)
        mock_conf_path.__truediv__ = mock.Mock(return_value=mock_minion_id_path)

        mock_salt_dir = mock.Mock(spec=Path)
        mock_salt_dir.__truediv__ = mock.Mock(return_value=mock_conf_path)

        mock_path_constants.salt_data_directory = mock_salt_dir

        return mock_minion_id_path

    @mock.patch("nisystemlink.clients.core.helpers._minion_id.PathConstants")
    def test__minion_id_file_exists__returns_content(self, mock_path_constants):
        """Test that the minion ID is read correctly when the file exists."""
        # Arrange
        expected_minion_id = "test-minion-123"
        mock_minion_id_path = self._setup_mock_path(mock_path_constants, exists=True)

        # Mock the file open and read
        mock_open = mock.mock_open(read_data=f"{expected_minion_id}\n")

        # Act
        with mock.patch("builtins.open", mock_open):
            result = read_minion_id()

        # Assert
        assert result == expected_minion_id
        mock_minion_id_path.exists.assert_called_once()
        mock_open.assert_called_once_with(mock_minion_id_path, "r", encoding="utf-8")

    @mock.patch("nisystemlink.clients.core.helpers._minion_id.PathConstants")
    def test__minion_id_file_exists_with_whitespace__returns_stripped_content(
        self, mock_path_constants
    ):
        """Test that the minion ID is stripped of leading/trailing whitespace."""
        # Arrange
        expected_minion_id = "test-minion-456"
        mock_minion_id_path = self._setup_mock_path(mock_path_constants, exists=True)

        # Mock the file open with extra whitespace
        mock_open = mock.mock_open(read_data=f"  {expected_minion_id}  \n\t")

        # Act
        with mock.patch("builtins.open", mock_open):
            result = read_minion_id()

        # Assert
        assert result == expected_minion_id
        mock_minion_id_path.exists.assert_called_once()

    @mock.patch("nisystemlink.clients.core.helpers._minion_id.PathConstants")
    def test__minion_id_file_does_not_exist__returns_none(self, mock_path_constants):
        """Test that None is returned when the minion_id file does not exist."""
        # Arrange
        mock_minion_id_path = self._setup_mock_path(mock_path_constants, exists=False)

        # Act
        result = read_minion_id()

        # Assert
        assert result is None
        mock_minion_id_path.exists.assert_called_once()

    @mock.patch("nisystemlink.clients.core.helpers._minion_id.PathConstants")
    def test__minion_id_file_has_oserror__returns_none(self, mock_path_constants):
        """Test that None is returned when an OSError occurs reading the file."""
        # Arrange
        mock_minion_id_path = self._setup_mock_path(mock_path_constants, exists=True)

        # Mock the file open to raise OSError
        mock_open = mock.mock_open()
        mock_open.side_effect = OSError("File access error")

        # Act
        with mock.patch("builtins.open", mock_open):
            result = read_minion_id()

        # Assert
        assert result is None
        mock_minion_id_path.exists.assert_called_once()

    @mock.patch("nisystemlink.clients.core.helpers._minion_id.PathConstants")
    def test__minion_id_file_has_permission_error__returns_none(
        self, mock_path_constants
    ):
        """Test that None is returned when a PermissionError occurs reading the file."""
        # Arrange
        mock_minion_id_path = self._setup_mock_path(mock_path_constants, exists=True)

        # Mock the file open to raise PermissionError
        mock_open = mock.mock_open()
        mock_open.side_effect = PermissionError("Permission denied")

        # Act
        with mock.patch("builtins.open", mock_open):
            result = read_minion_id()

        # Assert
        assert result is None
        mock_minion_id_path.exists.assert_called_once()

    @mock.patch("nisystemlink.clients.core.helpers._minion_id.PathConstants")
    def test__minion_id_file_is_empty__returns_empty_string(self, mock_path_constants):
        """Test that an empty string is returned when the file is empty."""
        # Arrange
        mock_minion_id_path = self._setup_mock_path(mock_path_constants, exists=True)

        # Mock the file open with empty content
        mock_open = mock.mock_open(read_data="")

        # Act
        with mock.patch("builtins.open", mock_open):
            result = read_minion_id()

        # Assert
        assert result == ""
        mock_minion_id_path.exists.assert_called_once()

    @mock.patch("nisystemlink.clients.core.helpers._minion_id.PathConstants")
    def test__minion_id_file_only_whitespace__returns_empty_string(
        self, mock_path_constants
    ):
        """Test that an empty string is returned when the file contains only whitespace."""
        # Arrange
        mock_minion_id_path = self._setup_mock_path(mock_path_constants, exists=True)

        # Mock the file open with only whitespace
        mock_open = mock.mock_open(read_data="   \n\t  \n")

        # Act
        with mock.patch("builtins.open", mock_open):
            result = read_minion_id()

        # Assert
        assert result == ""
        mock_minion_id_path.exists.assert_called_once()
