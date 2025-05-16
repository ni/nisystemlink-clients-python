from nisystemlink.clients.core._uplink._json_model import JsonModel
from ._state import State
from ...models._execution_definition import ExecutionDefinition


class ActionTransitionDefinition(JsonModel):
    """Represents a transition between workflow states triggered by a specific action."""

    action: str
    """The name of the action that triggers the transition."""

    nextState: State
    """The state to transition to after the action is performed."""

    nextSubstate: str
    """The substate to transition to within the next state."""

    showInUI: bool
    """Indicates whether this transition should be visible in the user interface."""


class SubstateDefinition(JsonModel):
    """Represents a substate within a workflow definition."""

    id: str
    """The unique identifier for the substate."""

    label: str
    """The display label for the substate."""

    availableActions: list[ActionTransitionDefinition]
    """List of actions that can be performed from this substate."""


class StateDefinition(JsonModel):
    """Represents the definition of a workflow state within a test plan."""

    state: State
    """The state associated with this definition."""

    dashboardAvailable: bool
    """Indicates if the state is available on the dashboard."""

    defaultSubstate: str
    """The name of the default substate for this state."""

    substates: list[SubstateDefinition]
    """A list of substates defined for this state."""


class ActionDefinition(JsonModel):
    """Represents the definition of an action within a workflow."""

    id: str
    """The unique identifier for the action."""

    label: str
    """The display label for the action."""

    executionAction: ExecutionDefinition
    """The execution details associated with the action."""


class WorkflowDefinition(JsonModel):
    """Contains information about a workflow definition."""

    actions: list[ActionDefinition]
    """A list of action definitions in the workflow."""

    states: list[StateDefinition]
    """A list of state definitions in the workflow."""
