"""Implementation of Alarm Client"""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from uplink import Field, retry

from . import models


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class AlarmClient(BaseClient):

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
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
    def acknowledge_alarm(
        self, instance_ids: list[str], force_clear: bool = False
    ) -> models.AcknowledgeByInstanceIdResponse:
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

    @post("instances", return_key="instanceId")
    def create_or_update_alarm(self, request: models.CreateOrUpdateAlarmRequest) -> str:
        """Creates or updates an instance, or occurrence, of an alarm.

        Creates or updates an alarm based on the requested transition and the state
        of the current active alarm with the given alarm_id (specified in the request).
        Multiple calls with the same alarm_id will update the same alarm instance.

        Args:
            request: The request containing alarm_id (user-defined identifier),
                    transition details, and other alarm properties.

        Returns:
            The instance_id (unique occurrence identifier) of the created or modified alarm.
            Use this ID for operations like get_alarm(), delete_alarm(), or acknowledge.

        Raises:
            ApiException: if unable to communicate with the `/nialarm` Service or provided invalid arguments.
        """
        ...

    @get("instances/{instance_id}")
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

    @delete("instances/{instance_id}")
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
    def delete_instances_by_instance_id(
        self, instance_ids: list[str]
    ) -> models.DeleteByInstanceIdResponse:
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
        self, request: models.QueryWithFilterRequest
    ) -> models.QueryWithFilterResponse:
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
