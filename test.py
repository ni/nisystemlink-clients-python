from re import M
from typing import Any, Optional
from pydantic import BaseModel, Extra


class Measurement(BaseModel):
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
        print(self.__fields__)
        print(data)
        processed_data = {
            k: str(v) if k not in self.__fields__ else v for k, v in data.items()
        }
        super().__init__(**processed_data)

meas = Measurement(name="test", status="pass", measurement="test", lowLimit="0", highLimit="1", units="test", comparisonType="test", specInfo={"specKey": 10})
print(meas)