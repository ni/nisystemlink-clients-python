from typing import List

from nisystemlink.clients.testmonitor.models._create_steps_request import (
    BaseStepRequest,
)


class UpdateStepRequest(BaseStepRequest):
    name: str | None = None
    """Step name."""

    children: List["UpdateStepRequest"] | None = None
    """Nested child steps."""
