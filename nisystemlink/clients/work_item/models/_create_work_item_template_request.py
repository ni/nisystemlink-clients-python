from ._work_item_template import WorkItemTemplateBase


class CreateWorkItemTemplateRequest(WorkItemTemplateBase):
    """Represents the request body content for creating a work item template."""

    name: str
    """The name of the work item template."""

    template_group: str
    """The template group defined by the user."""

    type: str
    """The type of work item created from this template."""
