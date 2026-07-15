# -*- coding: utf-8 -*-

"""Implementation of JupyterHttpConfiguration."""

import os
import sys

from nisystemlink.clients import core


class JupyterHttpConfiguration(core.HttpConfiguration):
    """An :class:`HttpConfiguration` for Jupyter notebooks running in a SystemLink environment."""

    _HTTP_URI_ENV_VAR = "SYSTEMLINK_HTTP_URI"
    _HTTP_API_KEY_ENV_VAR = "SYSTEMLINK_API_KEY"
    _SYSTEMLINK_SERVER_CERT_PATH = r"C:\ProgramData\National Instruments\Skyline\Certificates\http-server\http-server.cer"

    def __init__(self) -> None:
        """Initialize a configuration for SystemLink using API key-based
        authentication provided through environment variables.

        Raises:
            KeyError: if the expected environment variables are not set.
        """
        http_uri = os.environ[self._HTTP_URI_ENV_VAR]
        api_key = os.environ[self._HTTP_API_KEY_ENV_VAR]

        if sys.platform.startswith("win"):
            super().__init__(
                http_uri, api_key, cert_path=self._SYSTEMLINK_SERVER_CERT_PATH
            )
        else:
            super().__init__(http_uri, api_key)
