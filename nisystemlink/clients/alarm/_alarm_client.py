"""Implementation of Alarm Client"""

from typing import List, Literal, overload

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from uplink import Field, Path, retry

from . import models


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class AlarmClient(BaseClient):

    def __init__(self, configuration: core.HttpConfiguration | None = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/nialarm/v1/")

    @post(
        "acknowledge-instances-by-instance-id",
        args=[Field("instanceIds"), Field("forceClear")],
    )
    def acknowledge_alarms(
        self, instance_ids: List[str], *, force_clear: bool = False
    ) -> models.AcknowledgeAlarmsResponse:
        """Acknowledges one or more alarm instances by their instance IDs.

        Args:
            instance_ids: List of instance IDs (unique occurrence identifiers) of the alarms to acknowledge.
                 These are the server-generated IDs returned when creating/updating alarms,
                 not the user-defined alarm_id.
            force_clear: Whether or not the affected alarms should have their clear field set to true.
                         Defaults to False.

        Returns:
            A response containing the instance IDs that were successfully acknowledged,
            the instance IDs that failed, and error details for failures.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service or provided invalid arguments.
        """
        ...

    @overload
    def create_or_update_alarm(  # noqa: E704
        self,
        request: models.CreateOrUpdateAlarmRequest,
        *,
        ignore_conflict: Literal[False] = False,
    ) -> str: ...

    @overload
    def create_or_update_alarm(  # noqa: E704
        self,
        request: models.CreateOrUpdateAlarmRequest,
        *,
        ignore_conflict: Literal[True],
    ) -> str | None: ...

    def create_or_update_alarm(
        self,
        request: models.CreateOrUpdateAlarmRequest,
        *,
        ignore_conflict: bool = False,
    ) -> str | None:
        """Creates or updates an instance, or occurrence, of an alarm.

        Creates or updates an alarm based on the requested transition and the state
        of the current active alarm with the given alarm_id (specified in the request).
        Multiple calls with the same alarm_id will update the same alarm instance.

        Args:
            request: The request containing alarm_id (user-defined identifier),
                    transition details, and other alarm properties.
            ignore_conflict: If True, 409 Conflict errors will be ignored and None will be returned.
                           If False (default), 409 errors will raise an ApiException.
                           Setting this to True is useful for stateless applications that want to
                           attempt state transitions without checking the current alarm state first.

        Returns:
            The instance_id (unique occurrence identifier) of the created or modified alarm.
            Use this ID for operations like get_alarm(), delete_alarm(), or acknowledge.
            Returns None if ignore_conflict is True and a 409 Conflict occurs.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service or provided invalid arguments.
                A 409 Conflict error occurs when the request does not represent a valid transition
                for an existing alarm, such as attempting to clear an alarm which is already clear,
                or attempting to set an alarm which is already set at the given severity level.
                This error can be suppressed by setting ignore_conflict=True.
        """
        try:
            return self._create_or_update_alarm(request)
        except core.ApiException as e:
            if ignore_conflict and e.http_status_code == 409:
                return None
            raise

    @post("instances", return_key="instanceId")
    def _create_or_update_alarm(
        self, request: models.CreateOrUpdateAlarmRequest
    ) -> str:
        """Internal implementation of create_or_update_alarm."""
        ...

    @get("instances/{instance_id}", args=[Path("instance_id")])
    def get_alarm(self, instance_id: str) -> models.Alarm:
        """Gets an alarm by its instance_id.

        Args:
            instance_id: The unique instance ID (occurrence identifier) of the alarm to retrieve.
                This is the server-generated ID returned from create_or_update_alarm(),
                not the user-defined alarm_id.

        Returns:
            The alarm with the specified instance_id.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service or provided invalid arguments.
        """
        ...

    @delete("instances/{instance_id}", args=[Path("instance_id")])
    def delete_alarm(self, instance_id: str) -> None:
        """Deletes an alarm by its instance_id.

        Args:
            instance_id: The unique instance ID (occurrence identifier) of the alarm to delete.
                This is the server-generated ID returned from create_or_update_alarm(),
                not the user-defined alarm_id.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service or provided invalid arguments.
        """
        ...

    @post("delete-instances-by-instance-id", args=[Field("instanceIds")])
    def delete_alarms(self, instance_ids: List[str]) -> models.DeleteAlarmsResponse:
        """Deletes multiple alarm instances by their instance IDs.

        Args:
            instance_ids: List of instance IDs (unique occurrence identifiers) of the alarms to delete.
                 These are the server-generated IDs returned when creating/updating alarms,
                 not the user-defined alarm_id.

        Returns:
            A response containing lists of successfully deleted and failed instance IDs,
            along with error information for failures.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service or provided invalid arguments.
        """
        ...

    @post("query-instances-with-filter")
    def query_alarms(
        self, request: models.QueryAlarmsWithFilterRequest
    ) -> models.QueryAlarmsWithFilterResponse:
        """Queries for instances, or occurrences, of alarms using Dynamic LINQ.

        Specifying an empty JSON object in the request body will result in all alarms being returned.

        Args:
            request: The request containing filter information and query options.

        Returns:
            A response containing the list of alarms that match the query, along with
            optional total count and continuation token for pagination.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service or provided invalid arguments.
        """
        ...
