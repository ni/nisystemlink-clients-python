from typing import Any, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Extra


class Measurement(JsonModel):
    name: Optional[str] = None
    status: Optional[str] = None
    measurement: Optional[str] = None
    lowLimit: Optional[str] = None
    highLimit: Optional[str] = None
    units: Optional[str] = None
    comparisonType: Optional[str] = None

    class Config:
        extra = Extra.allow

    def __init__(self, **data: Any) -> None:
        # Convert all extra fields to str while keeping known fields unchanged
        processed_data = {
            k: str(v) if k not in self.__fields__ else v for k, v in data.items()
        }
        super().__init__(**processed_data)


class StepData(JsonModel):
    text: Optional[str] = None
    """Text string describing the output data."""

    parameters: Optional[List[Measurement]] = None
    """List of properties objects."""
