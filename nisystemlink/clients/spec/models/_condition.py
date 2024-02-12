from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Extra, Field


class ConditionType(Enum):
    NUMERIC = "NUMERIC"
    STRING = "STRING"


class ConditionRange(JsonModel):
    class Config:
        extra = Extra.forbid

    min: Optional[float] = Field(None, example=50)
    """
    Minimum value of the condition range.
    """
    max: Optional[float] = Field(None, example=600)
    """
    Maximum value of the condition range.
    """
    step: Optional[float] = Field(None, example=25.55)
    """
    Step value of the condition range.
    """


class ConditionValueBase(JsonModel):
    class Config:
        extra = Extra.forbid

    condition_type: ConditionType = Field(..., alias="conditionType")
    """
    Type of the Condition.
    """


class NumericConditionValue(ConditionValueBase):
    class Config:
        extra = Extra.forbid

    range: Optional[List[ConditionRange]] = None
    """
    List of condition range values.
    """
    discrete: Optional[List[float]] = Field(None, example=[-55, 66.6])
    """
    List of condition discrete values.
    """
    unit: Optional[str] = Field(None, example="mV")
    """
    Unit of the condition.
    """


class StringConditionValue(ConditionValueBase):
    class Config:
        extra = Extra.forbid

    discrete: Optional[List[str]] = None
    """
    List of condition discrete values.
    """


class Condition(JsonModel):
    class Config:
        extra = Extra.forbid

    name: Optional[str] = Field(None, example="InputVoltage")
    """
    Name of the condition.
    """
    value: Optional[Union[NumericConditionValue, StringConditionValue]] = None
    """
    Value of the condition.
    """
