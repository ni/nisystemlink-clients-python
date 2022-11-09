from systemlink.clients import core
from uplink import Consumer


class BaseClient(Consumer):
    def __init__(self, configuration: core.HttpConfiguration):
        super().__init__(base_url=configuration.server_uri)
        if configuration.api_keys:
            self.session.headers.update(configuration.api_keys)
