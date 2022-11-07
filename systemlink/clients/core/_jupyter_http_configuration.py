# -*- coding: utf-8 -*-

"""Implementation of JupyterHttpConfiguration."""

import os

from systemlink.clients import core


class JupyterHttpConfiguration(core.HttpConfiguration):
    """An :class:`HttpConfiguration` specifically for use in Jupyter notebooks."""

    _HTTP_URI_ENV_VAR = "SYSTEMLINK_HTTP_URI"
    _HTTP_API_KEY_ENV_VAR = "SYSTEMLINK_API_KEY"

    def __init__(self) -> None:
        """Initialize a configuration for SystemLink using API key-based
        authentication provided through environment variables.

        Raises:
            KeyError: if the expected environment variables are not set.
        """
        super().__init__(
            os.environ[self._HTTP_URI_ENV_VAR], os.environ[self._HTTP_API_KEY_ENV_VAR]
        )
