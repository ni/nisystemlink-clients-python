# -*- coding: utf-8 -*-

"""Tests for HttpConfiguration."""

import pathlib

import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration


class TestHttpConfiguration:
    """Test cases for HttpConfiguration class."""

    def test__valid_server_uri__initializes_correctly(self):
        """Test that a valid server URI initializes the configuration correctly."""
        config = HttpConfiguration("https://example.com")

        assert config.server_uri == "https://example.com"
        assert config.api_keys is None
        assert config.username is None
        assert config.password is None
        assert config.cert_path is None
        assert config.workspace is None
        assert config.verify is True
        assert (
            config.timeout_milliseconds
            == HttpConfiguration.DEFAULT_TIMEOUT_MILLISECONDS
        )
        assert config.user_agent is None

    def test__server_uri_with_port__preserves_port(self):
        """Test that server URI with port preserves the port."""
        config = HttpConfiguration("https://example.com:8080")

        assert config.server_uri == "https://example.com:8080"

    def test__server_uri_with_path_and_query__strips_path_and_query(self):
        """Test that path and query components are stripped from server URI."""
        config = HttpConfiguration("https://example.com/path?query=value")

        assert config.server_uri == "https://example.com"

    def test__api_key_authentication__sets_api_keys(self):
        """Test that API key authentication sets the api_keys property."""
        config = HttpConfiguration("https://example.com", api_key="test-key")

        assert config.api_keys == {"x-ni-api-key": "test-key"}
        assert config.username is None
        assert config.password is None

    def test__username_password_authentication__sets_credentials(self):
        """Test that username/password authentication sets credentials."""
        config = HttpConfiguration(
            "https://example.com", username="testuser", password="testpass"
        )

        assert config.username == "testuser"
        assert config.password == "testpass"
        assert config.api_keys is None

    def test__all_optional_parameters__sets_all_properties(self):
        """Test that all optional parameters are set correctly."""
        cert_path = pathlib.Path("/path/to/cert.pem")
        config = HttpConfiguration(
            "https://example.com",
            api_key="test-key",
            cert_path=cert_path,
            workspace="workspace-123",
            verify=False,
        )

        assert config.server_uri == "https://example.com"
        assert config.api_keys == {"x-ni-api-key": "test-key"}
        assert config.cert_path == cert_path
        assert config.workspace == "workspace-123"
        assert config.verify is False

    def test__missing_scheme__raises_value_error(self):
        """Test that missing scheme in server URI raises ValueError."""
        with pytest.raises(ValueError, match="Scheme.*not included"):
            HttpConfiguration("example.com")

    def test__missing_hostname__raises_value_error(self):
        """Test that missing hostname in server URI raises ValueError."""
        with pytest.raises(ValueError, match="Host.*not included"):
            HttpConfiguration("https://")

    def test__username_without_password__raises_value_error(self):
        """Test that username without password raises ValueError."""
        with pytest.raises(
            ValueError, match="If username or password is set, both must be set"
        ):
            HttpConfiguration("https://example.com", username="testuser")

    def test__password_without_username__raises_value_error(self):
        """Test that password without username raises ValueError."""
        with pytest.raises(
            ValueError, match="If username or password is set, both must be set"
        ):
            HttpConfiguration("https://example.com", password="testpass")

    def test__timeout_milliseconds_property__getter_and_setter(self):
        """Test timeout_milliseconds property getter and setter."""
        config = HttpConfiguration("https://example.com")

        # Test default value
        assert (
            config.timeout_milliseconds
            == HttpConfiguration.DEFAULT_TIMEOUT_MILLISECONDS
        )

        # Test setter
        config.timeout_milliseconds = 30000
        assert config.timeout_milliseconds == 30000

    def test__user_agent_property__getter_and_setter(self):
        """Test user_agent property getter and setter."""
        config = HttpConfiguration("https://example.com")

        # Test default value
        assert config.user_agent is None

        # Test setter with value
        config.user_agent = "TestAgent/1.0"
        assert config.user_agent == "TestAgent/1.0"

        # Test setter with None
        config.user_agent = None
        assert config.user_agent is None

        # Test setter with empty string
        config.user_agent = ""
        assert config.user_agent is None

    def test__verify_property__getter_and_setter(self):
        """Test verify property getter and setter."""
        config = HttpConfiguration("https://example.com")

        # Test default value
        assert config.verify is True

        # Test setter
        config.verify = False
        assert config.verify is False

        config.verify = True
        assert config.verify is True

    def test__api_keys_property__returns_copy(self):
        """Test that api_keys property returns a copy of the internal dictionary."""
        config = HttpConfiguration("https://example.com", api_key="test-key")

        api_keys = config.api_keys
        assert api_keys == {"x-ni-api-key": "test-key"}

        # Modify the returned dictionary
        api_keys["new-key"] = "new-value"

        # Original should be unchanged
        assert config.api_keys == {"x-ni-api-key": "test-key"}

    def test__api_keys_property__returns_none_when_no_api_key(self):
        """Test that api_keys property returns None when no API key is set."""
        config = HttpConfiguration("https://example.com")

        assert config.api_keys is None

    def test__server_uri_property__is_read_only(self):
        """Test that server_uri property is read-only."""
        config = HttpConfiguration("https://example.com")

        # These properties should only have getters, not setters
        # We can test this by trying to set and expecting an AttributeError
        with pytest.raises(AttributeError):
            config.server_uri = "https://different.com"

    def test__username_property__is_read_only(self):
        """Test that username property is read-only."""
        config = HttpConfiguration(
            "https://example.com", username="test", password="test"
        )

        # Username should be read-only after initialization
        with pytest.raises(AttributeError):
            config.username = "different"

    def test__password_property__is_read_only(self):
        """Test that password property is read-only."""
        config = HttpConfiguration(
            "https://example.com", username="test", password="test"
        )

        # Password should be read-only after initialization
        with pytest.raises(AttributeError):
            config.password = "different"

    def test__cert_path_property__is_read_only(self):
        """Test that cert_path property is read-only."""
        config = HttpConfiguration("https://example.com")

        # Cert path should be read-only after initialization
        with pytest.raises(AttributeError):
            config.cert_path = pathlib.Path("/different/path")

    def test__workspace_property__is_read_only(self):
        """Test that workspace property is read-only."""
        config = HttpConfiguration("https://example.com")

        # Workspace should be read-only after initialization
        with pytest.raises(AttributeError):
            config.workspace = "different-workspace"

    def test__default_timeout_constant__has_expected_value(self):
        """Test that the default timeout constant has the expected value."""
        assert HttpConfiguration.DEFAULT_TIMEOUT_MILLISECONDS == 60000

    def test__http_scheme__is_accepted(self):
        """Test that HTTP scheme is accepted."""
        config = HttpConfiguration("http://example.com")

        assert config.server_uri == "http://example.com"

    def test__case_insensitive_scheme__is_normalized_to_lowercase(self):
        """Test that case-insensitive schemes are normalized to lowercase."""
        config = HttpConfiguration("HTTPS://example.com")

        assert config.server_uri == "https://example.com"

    def test__ipv4_address__is_accepted(self):
        """Test that IPv4 addresses are accepted as hostnames."""
        config = HttpConfiguration("https://192.168.1.1")

        assert config.server_uri == "https://192.168.1.1"

    def test__ipv6_address__is_accepted(self):
        """Test that IPv6 addresses are accepted as hostnames."""
        config = HttpConfiguration("https://[::1]")

        assert config.server_uri == "https://[::1]"

    def test__empty_api_key__does_not_set_api_keys(self):
        """Test that empty API key does not set api_keys."""
        config = HttpConfiguration("https://example.com", api_key="")

        assert config.api_keys is None

    def test__none_api_key__does_not_set_api_keys(self):
        """Test that None API key does not set api_keys."""
        config = HttpConfiguration("https://example.com", api_key=None)

        assert config.api_keys is None

    def test__pathlib_path__cert_path(self):
        """Test that pathlib.Path objects work for cert_path."""
        cert_path = pathlib.Path("/etc/ssl/certs/ca-bundle.crt")
        config = HttpConfiguration("https://example.com", cert_path=cert_path)

        assert config.cert_path == cert_path
        assert isinstance(config.cert_path, pathlib.Path)
