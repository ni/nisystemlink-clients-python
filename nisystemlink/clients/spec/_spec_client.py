"""Implementation of SpecClient"""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
from uplink import Field, retry

from . import models


@retry(
    when=retry.when.status([408, 429, 502, 503, 504]), stop=retry.stop.after_attempt(5)
)
class SpecClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Spec Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/nispec/v1/")

    @get("")
    def api_info(self) -> models.V1Operations:
        """Get information about available API operations.

        Returns:
            Information about available API operations.

        Raises:
            ApiException: if unable to communicate with the DataFrame Service.
        """
        ...

    @post("specs")
    def create_specs(
        self, specs: models.CreateSpecificationsRequest
    ) -> models.CreateSpecificationsPartialSuccess:
        """Creates one or more specifications.

        Args:
            specs: A list of specifications to create.

        Returns:
            A list of specs that were successfully created and ones that failed to be created.

        Raises:
            ApiException: if unable to communicate with the `/nispec` service or if there are
            invalid arguments.
        """
        ...

    @post("delete-specs", args=[Field("ids")])
    def delete_specs(
        self, ids: List[str]
    ) -> Optional[models.DeleteSpecificationsPartialSuccess]:
        """Deletes one or more specifications by global id.

        Args:
            ids: a list of specification ids. Note that these are the global ids and not the
            `specId` that is local to a product and workspace.

        Returns:
            None if all deletes succeed otherwise a list of which ids failed and which succeeded.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @post("query-specs")
    def query_specs(
        self, query: models.QuerySpecificationsRequest
    ) -> models.PagedSpecifications:
        """Queries for specs that match the filters.

        Args:
            query: The query contains a product id as well as a filter for specs under that product.

        Returns:
            A list of specifications that match the filter.
        """
        ...

    @post("update-specs")
    def update_specs(
        self, specs: models.UpdateSpecificationsRequest
    ) -> Optional[models.UpdateSpecificationsPartialSuccess]:
        """Updates one or more specifications.

        Update requires that the version field matches the version being updated from.

        Args:
            specs: a list of specifications that are to be updated. Must include the global id and
            each spec being updated must match the version currently on the server.

        Returns
            A list of specs that were successfully updated and a list of ones that were not along
            with error messages for updates that failed.
        """
        ...
