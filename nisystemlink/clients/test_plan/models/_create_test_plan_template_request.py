from ._test_plan_templates import TestPlanTemplateBase


class CreateTestPlanTemplateRequest(TestPlanTemplateBase):
    """Contains information about a test plan template request."""

    name: str
    """Name of the test plan template."""

    template_group: str
    """The template group defined by the user."""
