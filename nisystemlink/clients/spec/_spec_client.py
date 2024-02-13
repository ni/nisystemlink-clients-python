"""Implementation of SpecClient"""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post

from . import models


class SpecClient(BaseClient):
    def __init__(self, configuration: Optional[core.HttpConfiguration]):
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()
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
    ) -> models.CreateSpecificationsPartialSuccessResponse:
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

    @post("delete-specs")
    def delete_specs(
        self, spec_ids: models.DeleteSpecificationsRequest
    ) -> Optional[models.DeleteSpecificationsPartialSuccessResponse]:
        """Deletes one or more specifications by global id.

        Args:
            spec_ids: a list of specification ids. Note that these are the global ids and not the
            `specId` that is local to a product and workspace.

        Returns:
            None if all deletes succeed otherwise a list of which ids failed and which succeeded.

        Raises:
            ApiException: if unable to communicate with the `nispec` service or if there are invalid
            arguments.
        """
        ...

    @post("update-specs")
    def update_specs(
        self, specs: models.UpdateSpecificationsRequest
    ) -> Optional[models.UpdateSpecificationsPartialSuccessResponse]:
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
