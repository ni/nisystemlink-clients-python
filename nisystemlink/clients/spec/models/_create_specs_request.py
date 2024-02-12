from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.spec.models._specification import SpecificationBase
from pydantic import Extra, Field

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class CreateSpecificationsRequest(JsonModel):
    class Config:
        extra = Extra.forbid

    specs: Optional[List[CreateSpecificationRequestObject]] = None
    """
    List of specifications to be created.
    """


class CreateSpecificationRequestObject(SpecificationBase):
    pass

    class Config:
        extra = Extra.forbid


class CreateSpecificationResponseObject(JsonModel):
    class Config:
        extra = Extra.forbid

    id: Optional[str] = Field(None, example="6dfb2ce3741fe56d88838cc9")
    """
    The global ID of the specification.
    """
    product_id: Optional[str] = Field(
        None, alias="productId", example="110ac9e8-4187-9870-a0b4-10dabfa02a0e"
    )
    """
    Id of the product to which the specification is associated.
    """
    spec_id: Optional[str] = Field(None, alias="specId", example="Vsat01")
    """
    User provided value using which the specification is identified.
    This is unique for a product and workspace combination.
    """
    workspace: Optional[str] = Field(
        None, example="990ac9e8-41ac-9870-a0b4-10dddfa02a0e"
    )
    """
    Id of the workspace to which the specification is associated,
    """
    created_at: Optional[datetime] = Field(
        None, alias="createdAt", example="2018-05-09T15:07:42.527921Z"
    )
    """
    ISO-8601 formatted timestamp indicating when the specification was created.
    """
    created_by: Optional[str] = Field(
        None, alias="createdBy", example="0a9ca97e-23fc-4d71-b47e-e34b7a930f42"
    )
    """
    Id of the user who created the specification.
    """
    version: Optional[int] = Field(None, example=0)
    """
    Version of the specification. The initial version starts with 0.
    """


class CreateSpecificationsPartialSuccessResponse(JsonModel):
    class Config:
        extra = Extra.forbid

    created_specs: Optional[List[CreateSpecificationResponseObject]] = Field(
        None, alias="createdSpecs"
    )
    """
    Information about the created specification(s)
    """
    failed_specs: Optional[List[CreateSpecificationRequestObject]] = Field(
        None, alias="failedSpecs"
    )
    """
    List of specification requests that failed during creation.
    """
    error: Optional[ApiError] = None


CreateSpecificationsRequest.update_forward_refs()
