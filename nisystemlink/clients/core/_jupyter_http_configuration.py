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

        # SystemLink Server 26Q3 restricts notebook executions (by default). Access to the `HttpConfigurations` folder is
        # no longer granted for notebooks running under the JupyterHub/NotebookExecution services. Since config files under
        # `HttpConfigurations` are no longer readable, creating client objects from this library, from SLS notebooks,
        # will default to using this `JupyterHttpConfiguration`. However, this does not set a `cert_path`, so HTTPS
        # requests will fail.
        # When running SystemLink Server notebooks (Windows), we will therefore pass the Web Server CA certificate's path as the 
        # `cert_path`, if the file exists. This will allow clients created with the default configuration to use this CA certificate.
        # If the file does not exist (when the Web Server is configured in HTTP mode), do not pass it; an invalid `cert_path`
        # will lead to errors.
        if sys.platform.startswith("win") and os.path.exists(
            self._SYSTEMLINK_SERVER_CERT_PATH
        ):
            super().__init__(
                http_uri, api_key, cert_path=self._SYSTEMLINK_SERVER_CERT_PATH
            )
        else:
            super().__init__(http_uri, api_key)
