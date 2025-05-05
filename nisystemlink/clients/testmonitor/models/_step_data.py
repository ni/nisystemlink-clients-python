from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import ConfigDict, Field


class Measurement(JsonModel):
    name: Optional[str] = None
    status: Optional[str] = None
    measurement: Optional[str] = None
    lowLimit: Optional[str] = None
    highLimit: Optional[str] = None
    units: Optional[str] = None
    comparisonType: Optional[str] = None
    model_config = ConfigDict(extra="allow")
    __pydantic_extra__: Dict[str, str] = Field(init=False)


class StepData(JsonModel):
    text: Optional[str] = None
    """Text string describing the output data."""

    parameters: Optional[List[Measurement]] = None
    """List of properties objects."""
