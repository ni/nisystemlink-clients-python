from typing import Dict, List, Optional
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.test_plan.models._execution_definition import ExecutionDefinition

class DashboardReference(JsonModel):
    id: Optional[str] = None
    variables: Dict[str, str]

class Dashboard(JsonModel):
    id: Optional[str] = None
    variables: Dict[str, str]

class TestPlanTemplateBase(JsonModel):
    name: str
    templateGroup: str = None
    summary: Optional[str] = None
    productFamilies: Optional[List[str]] = None
    partNumbers: Optional[List[str]] = None
    description: Optional[str] = None
    testProgram: Optional[str] = None
    systemFilter: Optional[str] = None
    estimatedDurationInSeconds: Optional[int] = None
    workspace: Optional[str] = None
    properties: Optional[Dict[str, str]] = None
    fileIds: Optional[List[str]] = None
    dashboardReference: Optional[DashboardReference] = None
    dashboard: Optional[Dashboard] = None
    executionActions: Optional[List[ExecutionDefinition]] = None

class TestPlanTemplateResponse(TestPlanTemplateBase):
    id: Optional[str] = None
    name: Optional[str] = None