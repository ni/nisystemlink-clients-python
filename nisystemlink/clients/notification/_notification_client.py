"""Implementation of Notification Client"""

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import post
from uplink import retry

from . import models


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(1),
    on_exception=retry.CONNECTION_ERROR,
)
class NotificationClient(BaseClient):
    def __init__(self, configuration: core.HttpConfiguration | None = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the `/ninotification` service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/ninotification/v1/")

    @post("apply-dynamic-strategy")
    def apply_dynamic_notification_strategy(
        self, request: models.DynamicStrategyRequest
    ) -> None:
        """Applies the notification strategy from the given request.

        Args:
            request: Request with message template substitution fields and notification strategies.

        Returns:
            None.

        Raises:
            ApiException: if unable to communicate with the `/ninotification` service or provided invalid arguments.
        """
        ...
