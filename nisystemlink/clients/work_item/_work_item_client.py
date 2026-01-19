from typing import List

from nisystemlink.clients import core
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import get, post
from nisystemlink.clients.work_item import models
from uplink import Field, retry


@retry(
    when=retry.when.status(408, 429, 502, 503, 504),
    stop=retry.stop.after_attempt(5),
    on_exception=retry.CONNECTION_ERROR,
)
class WorkItemClient(BaseClient):
    def __init__(self, configuration: HttpConfiguration | None = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the WorkItem Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()

        super().__init__(configuration, base_path="/niworkitem/v1/")

    @get("workitems/{work_item_id}")
    def get_work_item(self, work_item_id: str) -> models.WorkItem:
        """Retrieves a work item by its ID.

        Args:
            work_item_id: The ID of the work item to retrieve.

        Returns:
            The work item corresponding to the given ID.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("workitems", args=[Field("workItems")])
    def create_work_items(
        self, work_items: List[models.CreateWorkItemRequest]
    ) -> models.CreateWorkItemsPartialSuccessResponse:
        """Creates one or more work items.

        Args:
            work_items: A list of work items to create.

        Returns:
            A list of created work items, work items that failed to create, and errors for failures.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("query-workitems")
    def query_work_items(
        self, query_work_items: models.QueryWorkItemsRequest
    ) -> models.PagedWorkItems:
        """Queries one or more work items.

        Args:
            query_work_items: The query request for work items.

        Returns:
            A list of work items based on the query.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("schedule-workitems")
    def schedule_work_items(
        self, schedule_work_items: models.ScheduleWorkItemsRequest
    ) -> models.ScheduleWorkItemsPartialSuccessResponse:
        """Schedule work items.

        Args:
            schedule_work_items: The schedule request for work item.

        Returns:
            A list of scheduled work items, work items that failed to schedule, and errors for failures.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("update-workitems")
    def update_work_items(
        self, update_work_items: models.UpdateWorkItemsRequest
    ) -> models.UpdateWorkItemsPartialSuccessResponse:
        """Updates one or more work items.

        Args:
            update_work_items: The update request containing work items to update.

        Returns:
            A list of updated work items, work items that failed to update, and errors for failures.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("delete-workitems", args=[Field("ids")])
    def delete_work_items(
        self, ids: List[str]
    ) -> models.DeleteWorkItemsPartialSuccessResponse | None:
        """Deletes one or more work items by IDs.

        Args:
            ids: A list of work item IDs to delete.

        Returns:
            A partial success if any work items failed to delete, or None if all
            work items were deleted successfully.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("workitem-templates", args=[Field("workItemTemplates")])
    def create_work_item_templates(
        self, work_item_templates: List[models.CreateWorkItemTemplateRequest]
    ) -> models.CreateWorkItemTemplatesPartialSuccessResponse:
        """Creates one or more work item templates.

        Args:
            work_item_templates: A list of work item templates to create.

        Returns:
            A list of created work item templates, templates that failed to create, and errors for failures.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("query-workitem-templates")
    def query_work_item_templates(
        self, query_work_item_templates: models.QueryWorkItemTemplatesRequest
    ) -> models.PagedWorkItemTemplates:
        """Queries one or more work item templates.

        Args:
            query_work_item_templates: The query request for work item templates.

        Returns:
            A list of work item templates based on the query.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("update-workitem-templates")
    def update_work_item_templates(
        self, update_work_item_templates: models.UpdateWorkItemTemplatesRequest
    ) -> models.UpdateWorkItemTemplatesPartialSuccessResponse:
        """Updates one or more work item templates.

        Args:
            update_work_item_templates: The update request containing work item templates to update.

        Returns:
            A list of updated work item templates, templates that failed to update, and errors for failures.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...

    @post("delete-workitem-templates", args=[Field("ids")])
    def delete_work_item_templates(
        self, ids: List[str]
    ) -> models.DeleteWorkItemTemplatesPartialSuccessResponse | None:
        """Deletes one or more work item templates.

        Args:
            ids: A list of work item template IDs to delete.

        Returns:
            A partial success if any work item templates failed to delete, or None if all
            work item templates were deleted successfully.

        Raises:
            ApiException: if unable to communicate with the `/niworkitem` service or provided invalid arguments.
        """
        ...
