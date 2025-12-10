from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import ConfigDict, Field


class Measurement(JsonModel):
    name: str | None = None
    status: str | None = None
    measurement: str | None = None
    lowLimit: str | None = None
    highLimit: str | None = None
    units: str | None = None
    comparisonType: str | None = None
    model_config = ConfigDict(extra="allow")
    __pydantic_extra__: Dict[str, str] = Field(init=False)


class StepData(JsonModel):
    text: str | None = None
    """Text string describing the output data."""

    parameters: List[Measurement] | None = None
    """List of properties objects."""
