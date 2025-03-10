from datetime import datetime, timezone
from typing import List

import pandas as pd
import pytest
from nisystemlink.clients.testmonitor.models import (
    NamedValue,
    Status,
    StatusType,
    Step,
    StepData,
)
from nisystemlink.clients.testmonitor.utilities import convert_steps_to_dataframe
from pandas import DataFrame


@pytest.fixture
def mock_steps_data() -> List[Step]:
    """Fixture to return a mock step data."""
    step1 = Step(
        name="MockStep1",
        step_type="StepType",
        step_id="5ffb2bf6771fa11e877838dd1",
        parent_id="5ffb2bf6771fa11e877838dd2",
        result_id="5ffb2bf6771fa11e877838dd3",
        path="Path",
        path_ids=["path_id_11", "path_id_12"],
        status=Status(status_type=StatusType.DONE, status_name="Done"),
        total_time_in_seconds=5,
        started_at=datetime(2023, 3, 27, 18, 39, 49, tzinfo=timezone.utc),
        updated_at=datetime(2024, 2, 2, 14, 22, 4, 625155, tzinfo=timezone.utc),
        inputs=[
            NamedValue(name="Input00", value="input_value_00"),
            NamedValue(name="Input11", value="input_value_11"),
            NamedValue(name="Input12", value="input_value_12"),
        ],
        outputs=[
            NamedValue(name="Output11", value="output_value_11"),
            NamedValue(name="Output12", value="output_value_12"),
        ],
        data_model="STDF",
        data=StepData(
            text="data1",
            parameters=[
                {
                    "name": "parameter_21",
                    "units": "A",
                    "status": "Passed",
                    "lowLimit": "6.0",
                    "highLimit": "21.0",
                    "measurement": "11.0",
                    "comparisonType": "GTLT",
                }
            ],
        ),
        has_children=False,
        workspace="846e294a-a007-47ac-9fc2-fac07eab240f",
        keywords=["keyword11", "keyword12"],
        properties={"property11": "property11_value", "property12": "property12_value"},
    )
    step2 = Step(
        name="MockStep2",
        step_type="StepType",
        step_id="5ffb2bf6771fa11e877838dd6",
        parent_id="5ffb2bf6771fa11e877838dd7",
        result_id="5ffb2bf6771fa11e877838dd8",
        path="Path",
        path_ids=["path_id_21", "path_id_22"],
        status=Status(status_type=StatusType.DONE, status_name="Done"),
        total_time_in_seconds=5,
        started_at=datetime(2023, 3, 27, 18, 39, 49, tzinfo=timezone.utc),
        updated_at=datetime(2024, 2, 2, 14, 22, 4, 625255, tzinfo=timezone.utc),
        inputs=[
            NamedValue(name="Input00", value="input_value_00"),
            NamedValue(name="Input21", value="input_value_21"),
            NamedValue(name="Input22", value="input_value_22"),
        ],
        outputs=[
            NamedValue(name="Output21", value="output_value_21"),
            NamedValue(name="Output22", value="output_value_22"),
        ],
        data_model="STDF",
        data=StepData(
            text="data2",
            parameters=[
                {
                    "name": "parameter_21",
                    "units": "A",
                    "status": "Passed",
                    "lowLimit": "6.0",
                    "highLimit": "21.0",
                    "measurement": "11.0",
                    "comparisonType": "GTLT",
                },
                {
                    "name": "parameter_22",
                    "units": "C",
                    "status": "Passed",
                    "lowLimit": "7.0",
                    "highLimit": "22.0",
                    "measurement": "12.0",
                    "comparisonType": "GTLT",
                },
            ],
        ),
        has_children=True,
        workspace="846e294a-a007-47ac-9fc2-fac07eab240z",
        keywords=["keyword21", "keyword22"],
        properties={"property21": "property21_value", "property22": "property22_value"},
    )

    return [step1, step2]


@pytest.fixture
def expected_steps_dataframe(mock_steps_data: List[Step]) -> DataFrame:
    """Fixture to return the expected DataFrame based on the mock step data."""
    restructured_mock_steps = []

    for step in mock_steps_data:
        properties = (
            {f"properties.{key}": value for key, value in step.properties.items()}
            if step.properties
            else {}
        )
        inputs = (
            {f"inputs.{item.name}": item.value for item in step.inputs}
            if step.inputs
            else {}
        )
        outputs = (
            {f"outputs.{item.name}": item.value for item in step.outputs}
            if step.outputs
            else {}
        )

        if not (step.data and step.data.parameters):
            continue

        for parametric_data in step.data.parameters:
            parameter_data = {
                f"data.parameters.{key}": value
                for key, value in parametric_data.dict().items()
            }
            restructured_step = {
                "name": step.name,
                "step_type": step.step_type,
                "step_id": step.step_id,
                "parent_id": step.parent_id,
                "result_id": step.result_id,
                "path": step.path,
                "path_ids": step.path_ids,
                "total_time_in_seconds": step.total_time_in_seconds,
                "started_at": step.started_at,
                "updated_at": step.updated_at,
                "data_model": step.data_model,
                "has_children": step.has_children,
                "workspace": step.workspace,
                "keywords": step.keywords,
                "status.status_type": step.status.status_type if step.status else None,
                "status.status_name": step.status.status_name if step.status else None,
                **inputs,
                **outputs,
                "data.text": step.data.text,
                **parameter_data,
                **properties,
            }
            restructured_mock_steps.append(restructured_step)

    expected_dataframe = DataFrame(restructured_mock_steps)
    expected_column_order = [
        "name",
        "step_type",
        "step_id",
        "parent_id",
        "result_id",
        "path",
        "path_ids",
        "total_time_in_seconds",
        "started_at",
        "updated_at",
        "data_model",
        "has_children",
        "workspace",
        "keywords",
        "status.status_type",
        "status.status_name",
        "inputs.Input00",
        "inputs.Input11",
        "inputs.Input12",
        "inputs.Input21",
        "inputs.Input22",
        "outputs.Output11",
        "outputs.Output12",
        "outputs.Output21",
        "outputs.Output22",
        "data.text",
        "data.parameters.name",
        "data.parameters.status",
        "data.parameters.measurement",
        "data.parameters.lowLimit",
        "data.parameters.highLimit",
        "data.parameters.units",
        "data.parameters.comparisonType",
        "properties.property11",
        "properties.property12",
        "properties.property21",
        "properties.property22",
    ]

    return expected_dataframe.reindex(columns=expected_column_order, copy=False)


@pytest.fixture
def empty_steps_data() -> List:
    """Fixture to return an empty list of steps."""
    return []


@pytest.mark.enterprise
@pytest.mark.unit
class TestTestMonitorDataframeUtilities:
    def test__convert_steps_to_dataframe__with_complete_data(
        self, mock_steps_data: List[Step], expected_steps_dataframe: DataFrame
    ):
        """Test normal case with valid step data."""
        steps_dataframe = convert_steps_to_dataframe(mock_steps_data)

        assert not steps_dataframe.empty
        assert (
            steps_dataframe.columns.to_list()
            == expected_steps_dataframe.columns.to_list()
        )
        assert steps_dataframe["updated_at"].dtype == "datetime64[ns, UTC]"
        assert steps_dataframe["started_at"].dtype == "datetime64[ns, UTC]"
        assert steps_dataframe["path_ids"].dtype == "object"
        assert isinstance(steps_dataframe["path_ids"].iloc[0], List)
        assert steps_dataframe["keywords"].dtype == "object"
        assert isinstance(steps_dataframe["keywords"].iloc[0], List)
        pd.testing.assert_frame_equal(
            steps_dataframe, expected_steps_dataframe, check_dtype=True
        )

    def test__convert_steps_to_dataframe__with_empty_data(self, empty_steps_data: List):
        """Test case when the input steps data is empty."""
        steps_dataframe = convert_steps_to_dataframe(empty_steps_data)

        assert steps_dataframe.empty

    def test__convert_steps_to_dataframe__with_missing_fields(
        self, mock_steps_data: List[Step], expected_steps_dataframe: DataFrame
    ):
        """Test case when some fields in step data are missing."""
        steps = mock_steps_data
        for step in steps:
            step.path_ids = None
            step.data = None
            step.inputs = None

        steps_dataframe = convert_steps_to_dataframe(steps)
        expected_steps_dataframe = expected_steps_dataframe.drop(
            columns=[
                "path_ids",
                "data.parameters.name",
                "data.parameters.units",
                "data.parameters.status",
                "data.parameters.lowLimit",
                "data.parameters.highLimit",
                "data.parameters.measurement",
                "data.parameters.comparisonType",
                "data.text",
                "inputs.Input00",
                "inputs.Input11",
                "inputs.Input12",
                "inputs.Input21",
                "inputs.Input22",
            ]
        )
        expected_steps_dataframe = expected_steps_dataframe.drop_duplicates(
            subset=["step_id", "result_id"], ignore_index=True
        )

        assert not steps_dataframe.empty
        assert (
            steps_dataframe.columns.to_list()
            == expected_steps_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            steps_dataframe, expected_steps_dataframe, check_dtype=True
        )
