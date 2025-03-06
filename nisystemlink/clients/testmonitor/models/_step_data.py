from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._status import Status
from pydantic import Extra


class Measurement(JsonModel):
    name: Optional[str] = None
    status: Optional[Status] = None
    measurement: Optional[str] = None
    lowLimit: Optional[str] = None
    highLimit: Optional[str] = None
    units: Optional[str] = None
    comparisonType: Optional[str] = None

    class Config:
        extra = Extra.allow


class StepData(JsonModel):
    text: Optional[str] = None
    """Text string describing the output data."""

    parameters: Optional[List[Measurement]] = None
    """List of properties objects."""
