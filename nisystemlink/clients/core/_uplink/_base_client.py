from nisystemlink.clients import core
from uplink import Consumer


class BaseClient(Consumer):
    """Base class for SystemLink clients, built on top of `Uplink <https://github.com/prkumar/uplink>`_."""

    def __init__(self, configuration: core.HttpConfiguration):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about how to connect.
        """
        super().__init__(base_url=configuration.server_uri)
        if configuration.api_keys:
            self.session.headers.update(configuration.api_keys)
