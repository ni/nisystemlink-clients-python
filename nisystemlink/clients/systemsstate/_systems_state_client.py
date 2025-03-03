"""Implementation of SystemsStateService Client"""

from io import BytesIO
from typing import Any, Dict, List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, patch, post
from uplink import Body, multipart, Part, Path, Query


from . import models


class SystemsStateClient(BaseClient):

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

        super().__init__(configuration, base_path="/nisystemsstate/v1/")

    def get_states(
        self,
        skip: Optional[int] = None,
        take: Optional[int] = None,
        workspace: Optional[str] = None,
        architecture: Optional[models.Architecture] = None,
        distribution: Optional[models.Distribution] = None,
    ) -> models.StateDescriptionListResponse:
        """Get the list of states

        Args:
            `skip`: Number of files to skip in the result when paging
            `take`: Number of files to return in the result
            `workspace`: The workspace id of the states
            `architecture`: The states that are compatible with the requested architecture
            `distribution`: The states that are compatible with the requested distribution

        Returns:
            The list of states for the given query parameters

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        """Uplink does not support enum serializing into str

        The below inner function is the uplink executable and the outer one acts as a wrapper function,
        which is exposed to the end user
        """

        @get(
            "states",
            args=[
                Query("Skip"),
                Query("Take"),
                Query("Workspace"),
                Query("Architecture"),
                Query("Distribution"),
            ],
        )
        def __get_states(
            self,
            skip: Optional[int] = None,
            take: Optional[int] = None,
            workspace: Optional[str] = None,
            architecture: Optional[str] = None,
            distribution: Optional[str] = None,
        ) -> models.StateDescriptionListResponse:
            """Uplink implementation"""
            ...

        return __get_states(
            self,
            skip=skip,
            take=take,
            workspace=workspace,
            architecture=architecture.value if architecture is not None else None,
            distribution=distribution.value if distribution is not None else None,
        )

    @post("states", args=[Body])
    def create_state(self, state: models.StateRequest) -> models.StateResponse:
        """Create state

        Args:
            `state`: Information about the state to be created.

        Returns:
            The state created

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    @post("export-state", args=[Body])
    def export_state(self, query: models.ExportStateRequest) -> str:
        """Generate state export

        Args:
            `query`: Contains identifying information on the state to export.

        Returns:
            The exported state as a file.

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    @post("export-state-from-system", args=[Body])
    def export_state_from_system(
        self, export_state_from_system_request: models.ExportStateFromSystemRequest
    ) -> str:
        """Generate state export of a system

        Args:
            `export_state_from_system_request`: Contains the system id from which to export the state.

        Returns:
            The exported state of the system as a file.

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    @get("states/{stateId}", args=[Path("stateId")])
    def get_state(self, id: str) -> models.StateResponse:
        """Get state based on the give stateId parameter

        Args:
            `id`: The respective id of the state

        Returns:
            The state of the given id

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    @patch("states/{stateId}", args=[Path("stateId"), Body])
    def update_state(
        self, id: str, patch_updates: Dict[str, Any]
    ) -> models.StateResponse:
        """Update an existing state

        Args:
            `id`: The respective id of the state to be updated
            `patch_updates`: A dictionary containing the properties to update, where
            keys are property names (strings) and values are the updated values.

        Returns:
            The updated state

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    @delete("states/{stateId}", args=[Path("stateId")])
    def delete_state(self, id: str) -> None:
        """Deleting an existing state

        Args:
            `id`: The respective id of the state to be deleted

        Returns:
            None

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    @post(
        "replace-state-content",
        args=[
            Part(name="Id", type=str),
            Part(name="ChangeDescription", type=str),
            Part(name="File", type=BytesIO),
        ],
    )
    def replace_state_content(
        self, id: str, change_description: str, file: BytesIO
    ) -> models.StateResponse:
        """Replace state content

        Args:
            `id`: The id of the state that is to have its content replaced.
            `change_description`: The description for this change.
            `file`: The state file (.sls) to get replaced with the existing one.

        Returns:
            The replaced state.

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    def import_state(
        self,
        name: str,
        description: str,
        distribution: models.Distribution,
        architecture: models.Architecture,
        properties: str,
        workspace: str,
        file: BytesIO,
    ) -> models.StateResponse:
        """Import state

        Args:
            `name`: The name of the state to be imported. Required.
            `description`: A description of the state.
            `distribution`: The distribution supported by the state. Required.
            `architecture`: The architecture supported by the state. Required.
            `properties`: Custom properties for the state, serialized as a JSON string.
            `workspace`: The ID of the workspace. Available starting with version 3 of
                the createOrUpdateStates operation.
            `file`: The state file (.sls) to be imported.

        Returns:
            The imported state.

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        """Uplink does not support enum serializing into str

        The below inner function is the uplink executable and the outer one acts as a wrapper function,
        which is exposed to the end user
        """

        @post(
            "import-state",
            args=[
                Part(name="Name", type=str),
                Part(name="Description", type=str),
                Part(name="Distribution", type=str),
                Part(name="Architecture", type=str),
                Part(name="Properties", type=str),
                Part(name="Workspace", type=str),
                Part(name="File", type=BytesIO),
            ],
        )
        def __import_state(
            self,
            name: str,
            description: str,
            distribution: str,
            architecture: str,
            properties: str,
            workspace: str,
            file: BytesIO,
        ) -> models.StateResponse:
            """Uplink implementation"""
            ...

        return __import_state(
            self,
            name=name,
            description=description,
            distribution=distribution.value if distribution is not None else None,
            architecture=architecture.value if architecture is not None else None,
            properties=properties,
            workspace=workspace,
            file=file,
        )

    @post("delete-states", args=[Body])
    def delete_states(self, ids: List[str]) -> None:
        """Delete multiple states

        Args:
            `ids`: A list of state ids for the states that are to be deleted.

        Returns:
            None.

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...
