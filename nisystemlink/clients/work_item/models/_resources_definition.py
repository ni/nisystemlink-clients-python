from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ResourceSelectionDefinition(JsonModel):
    """Selection metadata associated with the resource."""

    id: str | None = None
    """The ID of the resource reserved for the work item."""

    target_location_id: str | None = None
    """The ID of the location where the resource is to be moved."""

    target_system_id: str | None = None
    """The ID of the system where the resource is to be moved."""

    target_parent_id: str | None = None
    """The ID of the parent to which the resource is to be connected."""


class SystemResourceSelectionDefinition(JsonModel):
    """Selection metadata associated with the system resource."""

    id: str | None = None
    """The ID of the system reserved for the work item."""

    target_location_id: str | None = None
    """The ID of the location where the system is to be moved."""


class ResourceDefinition(JsonModel):
    """Resource reserved for the work item."""

    selections: List[ResourceSelectionDefinition] | None = None
    """Resource selections for the work item."""

    filter: str | None = None
    """The filter used to select the resources for the work item."""


class SystemResourceDefinition(JsonModel):
    """System resource reserved for the work item."""

    selections: List[SystemResourceSelectionDefinition] | None = None
    """System resource selections for the work item."""

    filter: str | None = None
    """The filter used to select the systems for the work item."""


class ResourcesDefinition(JsonModel):
    """Resources reserved for the work item."""

    assets: ResourceDefinition | None = None
    """Asset reservations for the work item."""

    duts: ResourceDefinition | None = None
    """DUT reservations for the work item."""

    fixtures: ResourceDefinition | None = None
    """Fixture reservations for the work item."""

    systems: SystemResourceDefinition | None = None
    """System reservations for the work item."""


class TemplateResourceDefinition(JsonModel):
    """Resource reserved for the work item created from a template."""

    filter: str | None = None
    """The filter used to select the resources for the work item."""


class TemplateResourcesDefinition(JsonModel):
    """Resources reserved for the work item created from a template."""

    assets: TemplateResourceDefinition | None = None
    """Asset reservations for the work item."""

    duts: TemplateResourceDefinition | None = None
    """DUT reservations for the work item."""

    fixtures: TemplateResourceDefinition | None = None
    """Fixture reservations for the work item."""

    systems: TemplateResourceDefinition | None = None
    """System reservations for the work item."""


class ScheduleResourceDefinition(JsonModel):
    """Resource reserved for scheduling the work item."""

    selections: List[ResourceSelectionDefinition] | None = None
    """Resource selections for the work item."""


class ScheduleSystemResourceDefinition(JsonModel):
    """System resource reserved for scheduling the work item."""

    selections: List[SystemResourceSelectionDefinition] | None = None
    """System resource selections for the work item."""


class ScheduleResourcesDefinition(JsonModel):
    """Resources reserved for scheduling the work item."""

    assets: ScheduleResourceDefinition | None = None
    """Asset reservations for the work item."""

    duts: ScheduleResourceDefinition | None = None
    """DUT reservations for the work item."""

    fixtures: ScheduleResourceDefinition | None = None
    """Fixture reservations for the work item."""

    systems: ScheduleSystemResourceDefinition | None = None
    """System reservations for the work item."""
