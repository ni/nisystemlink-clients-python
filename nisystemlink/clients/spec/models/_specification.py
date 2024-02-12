from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from ._condition import Condition, ConditionType
from pydantic import Extra, Field


class SpecificationLimit(JsonModel):
    class Config:
        extra = Extra.forbid

    min: Optional[float] = Field(None, example=-66.54)
    """
    Minimum value of the specification.
    """
    typical: Optional[float] = Field(None, example=180)
    """
    Typical value of the specification.
    """
    max: Optional[float] = Field(None, example=303.659)
    """
    Maximum value of the specification.
    """


class Type(Enum):
    PARAMETRIC = "PARAMETRIC"
    FUNCTIONAL = "FUNCTIONAL"


class SpecificationBase(JsonModel):
    class Config:
        extra = Extra.forbid

    product_id: str = Field(
        ...,
        alias="productId",
        example="110ac9e8-4187-9870-a0b4-10dabfa02a0e",
        min_length=1,
    )
    """
    Id of the product to which the specification will be associated.
    """
    spec_id: str = Field(..., alias="specId", example="Vsat01", min_length=1)
    """
    User provided value using which the specification will be identified.
    This should be unique for a product and workspace combination.
    """
    name: Optional[str] = Field(None, example="Saturation voltage")
    """
    Name of the specification.
    """
    category: Optional[str] = Field(None, example="Electrical characteristics")
    """
    Category of the specification.
    """
    type: Type = Field(..., example="PARAMETRIC")
    """
    Type of the specification.
    """
    symbol: Optional[str] = Field(None, example="VSat")
    """
    Short form identifier of the specification.
    """
    block: Optional[str] = Field(None, example="USB")
    """
    Block name of the specification.
    """
    limit: Optional[SpecificationLimit] = None
    unit: Optional[str] = Field(None, example="mV")
    """
    Unit of the specification.
    """
    conditions: Optional[List[Condition]] = None
    """
    Conditions associated with the specification.
    """
    keywords: Optional[List[str]] = Field(
        None, example=["Test specification only", "First"]
    )
    """
    Keywords or phrases associated with the specification.
    """
    properties: Optional[Dict[str, str]] = Field(
        None, example={"Product manager": "Jim", "Spec owner": "Jacob"}
    )
    """
    Properties associated with the specification.
    """
    workspace: Optional[str] = Field(
        None, example="990ac9e8-41ac-9870-a0b4-10dddfa02a0e"
    )
    """
    Id of the workspace to which the specification will be associated.
    Default workspace will be taken if the value is not given.
    """
