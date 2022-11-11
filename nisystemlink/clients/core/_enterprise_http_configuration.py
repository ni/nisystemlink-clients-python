# -*- coding: utf-8 -*-

"""Implementation of EnterpriseHttpConfiguration."""

from nisystemlink.clients import core


class EnterpriseHttpConfiguration(core.HttpConfiguration):
    """An :class:`HttpConfiguration` specifically for use with SystemLink Enterprise."""

    _ENTERPRISE_URI = "https://dev-api.lifecyclesolutions.ni.com"

    def __init__(self, api_key: str) -> None:
        """Initialize a configuration for SystemLink Enterprise using API key-based authentication.

        Args:
            api_key: The API key to send with requests.

        Raises:
            ValueError: if ``api_key`` is empty.
        """
        super().__init__(self._ENTERPRISE_URI, api_key=api_key)
