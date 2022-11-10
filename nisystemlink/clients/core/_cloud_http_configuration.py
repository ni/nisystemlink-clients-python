# -*- coding: utf-8 -*-

"""Implementation of CloudHttpConfiguration."""

from nisystemlink.clients import core


class CloudHttpConfiguration(core.HttpConfiguration):
    """An :class:`HttpConfiguration` specifically for use with SystemLink Cloud."""

    _CLOUD_URI = "https://api.systemlinkcloud.com"

    def __init__(self, api_key: str) -> None:
        """Initialize a configuration for SystemLink Cloud using API key-based authentication.

        Args:
            api_key: The API key to send with requests.

        Raises:
            ValueError: if ``api_key`` is empty.
        """
        super().__init__(self._CLOUD_URI, api_key=api_key)
