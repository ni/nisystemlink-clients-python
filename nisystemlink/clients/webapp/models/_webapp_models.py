# generated by datamodel-codegen:
#   filename:  <stdin>

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field, conint


class Type(Enum):
    DASHBOARD = "Dashboard"
    TILE_DASHBOARD = "TileDashboard"
    DASHBOARD_TEMPLATE = "DashboardTemplate"
    WEB_VI = "WebVI"
    VISUALIZATION = "Visualization"
    VISUALIZATION_TEMPLATE = "VisualizationTemplate"
    DATASPACE = "DataSpace"


class Shared(Enum):
    PRIVATE = "private"
    DIRECT = "direct"
    PUBLIC = "public"


class WebApp(JsonModel):
    id: Optional[str] = Field(None, example="asdsad-17a6-45323-b64b-65325287372d")
    """
    The webapp Id
    """
    type: Optional[Type] = None
    """
    The webapp type
    """
    name: Optional[str] = Field(None, example="My webapp")
    """
    The webapp name
    """
    workspace: Optional[str] = Field(
        None, example="0c80cf49-54e9-4e92-b117-3bfa574caa84"
    )
    """
    The Id of the workspace containing the webapp
    """
    user_id: Optional[str] = Field(
        None, alias="userId", example="d4f6b766-da45-4fe5-85c5-bd745c402cf9"
    )
    """
    The Id of the user that created the webapp
    """
    shared: Optional[Shared] = None
    """
    The webapp's sharing option
    """
    shared_emails: Optional[List[str]] = Field(None, alias="sharedEmails")
    """
    List of emails of users to share the webapp with. Applies when "shared" option is "direct"
    """
    policy_ids: Optional[List[str]] = Field(None, alias="policyIds")
    """
    List of policy Ids associated with the webapp, which give it access to the user's resources"
    """
    created: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The created timestamp (iso8601 format)
    """
    updated: Optional[datetime] = Field(None, example="2019-12-02T15:31:45.379Z")
    """
    The last updated timestamp (iso8601 format)
    """
    properties: Optional[Dict[str, Any]] = None
    """
    A map of key value properties associated with the webapp
    """


class WebAppContent(JsonModel):
    __root__: bytes = Field(..., title="WebApp Content")
    """
    The webapp binary content. Depending on the webapp's type it can be a dashboard, template or *.nipkg file exported from LabVIEW NXG
    """


class WebAppsAdvancedQuery(JsonModel):
    filter: Optional[str] = Field(
        None, example='name.StartsWith("myWebApp") || type == "WebVI"'
    )
    """
    The filter criteria for webapps, consisting of a string of queries composed using AND/OR operators. String values need to be enclosed in double quotes. Parenthesis can be used within the filter to better define the order of operations.

    Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'
    Operators:
    - Equals operator '='. Example: 'x = y'
    - Not equal operator '!='. Example: 'x != y'
    - Greater than operator '>'. Example: 'x > y'
    - Greater than or equal operator '>='. Example: 'x >= y'
    - Less than operator '<'. Example: 'x < y'
    - Less than or equal operator '<='. Example: 'x <= y'
    - Logical AND operator 'and'. Example: 'x and y'
    - Logical OR operator 'or'. Example: 'x or y'
    - Starts with operator '.StartsWith()', used to check whether a string starts with another string. Example: 'x.StartsWith(y)'
    - Does not start with operator '!.StartsWith()', used to check whether a string does not start with another string. Example: '!x.StartsWith(y)'
    - String null or empty 'string.IsNullOrEmpty()', used to check whether a string is null or empty. Example: 'string.IsNullOrEmpty(x)'
    - String is not null or empty '!string.IsNullOrEmpty()', used to check whether a string is not null or empty. Example: '!string.IsNullOrEmpty(x)'

    Valid webapp properties that can be used in the filter:
    - id
    - name
    - properties.embedLocation
    - properties.interface
    - shared
    - type
    - workspace
    """
    take: Optional[conint(ge=0, le=1000)] = Field(None, example=10)
    """
    The maximum number of webapps to return
    """
    continuation_token: Optional[str] = Field(
        None, alias="continuationToken", example="token"
    )
    """
    The continuation token can be used to paginate through the webapp query results. Provide this token in the next query webapps call.
    """


class Error(JsonModel):
    name: Optional[str] = None
    """
    String error code
    """
    code: Optional[int] = None
    """
    Numeric error code
    """
    message: Optional[str] = None
    """
    Complete error message
    """
    args: Optional[List[str]] = None
    """
    Positional argument values for the error code
    """
    inner_errors: Optional[List[Error]] = Field(None, alias="innerErrors")


Error.update_forward_refs()
