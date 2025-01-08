"""Implementation of SystemsStateService Client"""

from typing import Dict, List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, patch, post
from uplink import Body, Part, Path, Query

from . import models


class SystemsStateClient(BaseClient):
    # prevent pytest from thinking this is a test class
    __test__ = False

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
        ...

    @post("states", args=[Body])
    def create_state(self, new_state: models.StateRequest) -> models.StateResponse:
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
    def export_state(self, export_state_request: models.ExportStateRequest) -> str:
        """Generate state export

        Args:
            `export_state_request`: Contains identifying information on the state to export.

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
    def get_state(self, state_id: str) -> models.StateResponse:
        """Get state based on the give stateId parameter

        Args:
            `state_id`: The respective id of the state

        Returns:
            The state of the given id

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...

    @patch("states/{stateId}", args=[Path("stateId"), Body])
    def update_state(
        self, state_id: str, patch_updates: Dict[str, str]
    ) -> models.StateResponse:
        """Update an existing state

        Args:
            `state_id`: The respective id of the state to be updated
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
    def delete_state(self, state_id: str) -> None:
        """Deleting an existing state

        Args:
            `state_id`: The respective id of the state to be deleted

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
            Part(name="File", type=str),
        ],
    )
    def replace_state_content(
        self, id: str, change_description: str, file: str
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

    @post(
        "import-state",
        args=[
            Part(name="Name", type=str),
            Part(name="Description", type=str),
            Part(name="Distribution", type=str),
            Part(name="Architecture", type=str),
            Part(name="Properties", type=str),
            Part(name="Workspace", type=str),
            Part(name="File", type=str),
        ],
    )
    def import_state(
        self,
        name: str,
        description: str,
        distribution: str,
        architecture: str,
        properties: str,
        workspace: str,
        file: str,
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
        ...

    @post("delete-states", args=[Body])
    def delete_states(self, states_id_list: List[str]) -> None:
        """Delete multiple states

        Args:
            `states_id_list`: A list of state ids for the states that are to be deleted.

        Returns:
            None.

        Raises:
            ApiException : if unable to communicate with the ``/nisystemsstate`` Service
                or provided an invalid argument.
        """
        ...
