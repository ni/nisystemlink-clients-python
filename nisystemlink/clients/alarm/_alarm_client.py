"""Implementation of Alarm Client"""

from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from uplink import Path, retry

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
            ApiException: if unable to communicate with the Alarm Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()
        super().__init__(configuration, base_path="/nialarm/v1/")

    @post("acknowledge-instances-by-instance-id")
    def acknowledge_instances_by_instance_id(
        self, request: models.AcknowledgeByInstanceIdRequest
    ) -> models.AcknowledgeByInstanceIdResponse:
        """Acknowledges one or more alarm instances by their instance IDs.

        Args:
            request: The request containing instance IDs to acknowledge and optional force clear flag.

        Returns:
            A response containing the instance IDs that were successfully acknowledged,
            the instance IDs that failed, and error details for failures.

        Raises:
            ApiException: if unable to communicate with the Alarm Service or provided invalid arguments.
        """
        ...

    @post("instances")
    def create_or_update_alarm(
        self, request: models.CreateOrUpdateAlarmRequest
    ) -> models.CreateOrUpdateAlarmResponse:
        """Creates or updates an instance, or occurrence, of an alarm.

        Creates or updates an alarm based on the requested transition and the state 
        of the current active alarm with the given alarmId.

        Args:
            request: The request containing alarm information and transition details.

        Returns:
            A response containing the ID of the created or modified alarm.

        Raises:
            ApiException: if unable to communicate with the Alarm Service or provided invalid arguments.
        """
        ...

    @get("instances/{instance_id}")
    def get_alarm(self, instance_id: str) -> models.Alarm:
        """Gets an alarm by its instanceId.

        Args:
            instance_id: Unique ID of a particular instance, or occurrence, of an alarm.

        Returns:
            The alarm with the specified instance ID.

        Raises:
            ApiException: if unable to communicate with the Alarm Service or provided invalid arguments.
        """
        ...

    @delete("instances/{instance_id}")
    def delete_alarm(self, instance_id: str) -> None:
        """Deletes an alarm by its instanceId.

        Args:
            instance_id: Unique ID of a particular instance, or occurrence, of an alarm.

        Raises:
            ApiException: if unable to communicate with the Alarm Service or provided invalid arguments.
        """
        ...

    @post("delete-instances-by-instance-id")
    def delete_instances_by_instance_id(
        self, request: models.DeleteByInstanceIdRequest
    ) -> models.DeleteByInstanceIdResponse:
        """Deletes multiple alarm instances by their instanceIds.

        Args:
            request: Contains the instanceIds of the alarms to delete.

        Returns:
            A response containing lists of successfully deleted and failed instanceIds,
            along with error information for failures.

        Raises:
            ApiException: if unable to communicate with the Alarm Service or provided invalid arguments.
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
            ApiException: if unable to communicate with the Alarm Service or provided invalid arguments.
        """
        ...
