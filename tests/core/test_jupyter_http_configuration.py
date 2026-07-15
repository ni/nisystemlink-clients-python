import os
from unittest.mock import patch

from nisystemlink.clients.core import JupyterHttpConfiguration


_HTTP_URI_ENV_VAR = "SYSTEMLINK_HTTP_URI"
_HTTP_API_KEY_ENV_VAR = "SYSTEMLINK_API_KEY"
_SYSTEMLINK_SERVER_CERTIFICATE_PATH = (
    r"C:\ProgramData\National Instruments\Skyline"
    r"\Certificates\http-server\http-server.cer"
)
_SYSTEM_LINK_API_KEY_HEADER = "x-ni-api-key"


class TestJupyterHttpConfiguration:
    def test__cert_file_exists_on_windows__cert_path_is_passed(self):
        def mock_exists(path):
            if path == _SYSTEMLINK_SERVER_CERTIFICATE_PATH:
                return True
            return False

        with patch("sys.platform", "win32"):
            with patch("os.path.exists", side_effect=mock_exists):
                with patch.dict(
                    os.environ,
                    {
                        _HTTP_URI_ENV_VAR: "https://my-uri",
                        _HTTP_API_KEY_ENV_VAR: "my-api-key",
                    },
                ):
                    config = JupyterHttpConfiguration()
                    assert config.server_uri == "https://my-uri"
                    assert config.api_keys[_SYSTEM_LINK_API_KEY_HEADER] == "my-api-key"
                    assert config.cert_path == _SYSTEMLINK_SERVER_CERTIFICATE_PATH

    def test__cert_file_does_not_exist_on_windows__cert_path_is_not_passed(self):
        def mock_exists(path):
            if path == _SYSTEMLINK_SERVER_CERTIFICATE_PATH:
                return False
            return True

        with patch("sys.platform", "win32"):
            with patch("os.path.exists", side_effect=mock_exists):
                with patch.dict(
                    os.environ,
                    {
                        _HTTP_URI_ENV_VAR: "https://my-uri",
                        _HTTP_API_KEY_ENV_VAR: "my-api-key",
                    },
                ):
                    config = JupyterHttpConfiguration()
                    assert config.server_uri == "https://my-uri"
                    assert config.api_keys[_SYSTEM_LINK_API_KEY_HEADER] == "my-api-key"
                    assert config.cert_path is None

    def test__cert_file_exists_on_linux__cert_path_is_not_passed(self):
        def mock_exists(path):
            if path == _SYSTEMLINK_SERVER_CERTIFICATE_PATH:
                return True
            return False

        with patch("sys.platform", "linux"):
            with patch("os.path.exists", side_effect=mock_exists):
                with patch.dict(
                    os.environ,
                    {
                        _HTTP_URI_ENV_VAR: "https://my-uri",
                        _HTTP_API_KEY_ENV_VAR: "my-api-key",
                    },
                ):
                    config = JupyterHttpConfiguration()
                    assert config.server_uri == "https://my-uri"
                    assert config.api_keys[_SYSTEM_LINK_API_KEY_HEADER] == "my-api-key"
                    assert config.cert_path is None

    def test__cert_file_does_not_exist_on_linux__cert_path_is_not_passed(self):
        def mock_exists(path):
            if path == _SYSTEMLINK_SERVER_CERTIFICATE_PATH:
                return False
            return True

        with patch("sys.platform", "linux"):
            with patch("os.path.exists", side_effect=mock_exists):
                with patch.dict(
                    os.environ,
                    {
                        _HTTP_URI_ENV_VAR: "https://my-uri",
                        _HTTP_API_KEY_ENV_VAR: "my-api-key",
                    },
                ):
                    config = JupyterHttpConfiguration()
                    assert config.server_uri == "https://my-uri"
                    assert config.api_keys[_SYSTEM_LINK_API_KEY_HEADER] == "my-api-key"
                    assert config.cert_path is None
