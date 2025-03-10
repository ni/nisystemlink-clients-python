from typing import List, Optional

from nisystemlink.clients.testmonitor.models._create_steps_request import (
    BaseStepRequest,
)


class UpdateStepRequest(BaseStepRequest):
    name: Optional[str] = None
    """Step name."""

    children: Optional[List["UpdateStepRequest"]] = None
    """Nested child steps."""
