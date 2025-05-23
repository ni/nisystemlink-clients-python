"""Implementation of SystemsClient"""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import post
from uplink import Field, retry

from . import models


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class SystemsClient(BaseClient):

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Systems Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/nisysmgmt/v1/")

    @post("virtual")
    def create_virtual_system(
        self, create_virtual_system_request: models.CreateVirtualSystemRequest
    ) -> models.CreateVirtualSystemResponse:
        """Creates a virtual system.

        Args:
            alias: The alias of the virtual system.
            workspace: The workspace to create the virtual system in.

        Raises:
            ApiException: if unable to communicate with the `/nisysmgmt` service or provided invalid
                arguments.
        """
        ...

    @post("query-systems")
    def query_systems(
        self, query: models.QuerySystemsRequest
    ) -> models.QuerySystemsResponse:
        """Queries for systems that match the filter.

        Args:
            query : The query contains a DynamicLINQ query string in addition to other details
                about how to filter and return the list of systems.

        Returns:
            Response containing the list of systems that match the filter.

        Raises:
            ApiException: if unable to communicate with the `/nisysmgmt` Service or provided invalid
                arguments.
        """
        ...

    @post("remove-systems", args=[Field("tgt")])
    def remove_systems(self, tgt: List[str]) -> models.RemoveSystemsResponse:
        """Removes multiple systems.

        Args:
            virtual_system_to_remove : List of unique IDs of systems.

        Returns:
            A partial success if any systems failed to remove, or None if all
            systems were removed successfully.

        Raises:
            ApiException: if unable to communicate with the `/nisysmgmt` Service
                or provided an invalid argument.
        """
        ...
