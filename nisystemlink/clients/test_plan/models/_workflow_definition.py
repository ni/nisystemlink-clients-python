from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._execution_definition import ExecutionDefinition
from ._state import State


class ActionTransitionDefinition(JsonModel):
    """Represents a transition between workflow states triggered by a specific action."""

    action: str
    """The name of the action that triggers the transition."""

    next_state: State
    """The state to transition to after the action is performed."""

    next_substate: str
    """The substate to transition to within the next state."""

    show_in_UI: bool = Field(alias="showInUI")
    """Indicates whether this transition should be visible in the user interface."""


class SubstateDefinition(JsonModel):
    """Represents a substate within a workflow definition."""

    id: Optional[str] = None
    """The unique identifier for the substate."""

    label: Optional[str] = None
    """The display label for the substate."""

    available_actions: Optional[List[ActionTransitionDefinition]] = None
    """List of actions that can be performed from this substate."""


class StateDefinition(JsonModel):
    """Represents the definition of a workflow state within a test plan."""

    state: Optional[State] = None
    """The state associated with this definition."""

    dashboard_available: Optional[bool] = None
    """Indicates if the state is available on the dashboard."""

    default_substate: Optional[str] = None
    """The name of the default substate for this state."""

    substates: Optional[List[SubstateDefinition]] = None
    """A list of substates defined for this state."""


class ActionDefinition(JsonModel):
    """Represents the definition of an action within a workflow."""

    id: Optional[str] = None
    """The unique identifier for the action."""

    label: Optional[str] = None
    """The display label for the action."""

    execution_action: Optional[ExecutionDefinition] = None
    """The execution details associated with the action."""


class WorkflowDefinition(JsonModel):
    """Contains information about a workflow definition."""

    actions: Optional[List[ActionDefinition]] = None
    """A list of action definitions in the workflow."""

    states: Optional[List[StateDefinition]] = None
    """A list of state definitions in the workflow."""
