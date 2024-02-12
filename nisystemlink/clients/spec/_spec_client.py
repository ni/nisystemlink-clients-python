"""Implementation of SpecClient"""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
from uplink import Body

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

    @post("specs", args=[Body])
    def create_specs(
        self, specs: models.CreateSpecificationsRequest
    ) -> models.CreateSpecificationsPartialSuccessResponse: ...

    @post("delete-specs", args=[Body])
    def delete_specs(
        self, spec_ids: models.DeleteSpecificationsRequest
    ) -> Optional[models.DeleteSpecificationsPartialSuccessResponse]: ...
