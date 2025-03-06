from datetime import datetime
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
def mock_step_data() -> List[Step]:
    """Fixture to return a mock step data."""
    step = Step(
        name="MockStep",
        step_type="StepType",
        step_id="StepId",
        parent_id="ParentId",
        result_id="ResultId",
        path="Path",
        path_ids=["path_id_1", "path_id_2"],
        status=Status(status_type=StatusType.DONE, status_name="Done"),
        total_time_in_seconds=5,
        started_at=datetime(2023, 3, 27, 18, 39, 49),
        updated_at=datetime(2024, 2, 2, 14, 22, 4, 625155),
        inputs=[
            NamedValue(name="Input1", value="input_value_1"),
            NamedValue(name="Input2", value="input_value_2"),
        ],
        outputs=[
            NamedValue(name="Output1", value="output_value_1"),
            NamedValue(name="Output2", value="output_value_2"),
        ],
        data_model="STDF",
        data=StepData(
            text="",
            parameters=[
                {
                    "name": "parameter_1",
                    "units": "A",
                    "status": "Failed",
                    "lowLimit": "6.0",
                    "highLimit": "21.0",
                    "measurement": "11.0",
                    "comparisonType": "GTLT",
                }
            ],
        ),
        has_children=False,
        workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
        keywords=["keyword1", "keyword2"],
        properties={"property1": "property1_value", "property2": "property2_value"},
    )

    return [step]


@pytest.fixture
def expected_steps_dataframe(mock_step_data) -> DataFrame:
    """Fixture to return the expected DataFrame based on the mock step data."""
    step = mock_step_data[0]
    expected_dataframe_structure = {
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
        "status.status_type": step.status.status_type,
        "status.status_name": step.status.status_name,
        "inputs.Input1": step.inputs[0].value,
        "inputs.Input2": step.inputs[1].value,
        "outputs.Output1": step.outputs[0].value,
        "outputs.Output2": step.outputs[1].value,
        "data.text": step.data.text,
        "data.parameters": step.data.parameters,
        "properties.property1": step.properties.get("property1"),
        "properties.property2": step.properties.get("property2"),
    }

    return pd.json_normalize(expected_dataframe_structure)


@pytest.fixture
def empty_steps_data() -> List:
    """Fixture to return an empty list of steps."""
    return []


@pytest.mark.enterprise
@pytest.mark.unit
class TestTestMonitorDataframeUtilities:
    def test__convert_steps_to_dataframe__with_complete_data(
        self, mock_step_data, expected_steps_dataframe
    ):
        """Test normal case with valid step data."""
        steps_dataframe = convert_steps_to_dataframe(mock_step_data)

        assert not steps_dataframe.empty
        assert (
            steps_dataframe.columns.to_list()
            == expected_steps_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            steps_dataframe, expected_steps_dataframe, check_dtype=True
        )

    def test__convert_steps_to_dataframe__with_empty_data(self, empty_steps_data):
        """Test case when the input steps data is empty."""
        steps_dataframe = convert_steps_to_dataframe(empty_steps_data)

        assert steps_dataframe.empty

    def test__convert_steps_to_dataframe__with_missing_fields(
        self, mock_step_data, expected_steps_dataframe
    ):
        """Test case when some fields in step data are missing."""
        steps = mock_step_data
        steps[0].keywords = None
        steps[0].inputs = None

        steps_dataframe = convert_steps_to_dataframe(steps)
        expected_steps_dataframe = expected_steps_dataframe.drop(
            columns=["keywords", "inputs.Input1", "inputs.Input2"]
        )

        assert not steps_dataframe.empty
        assert (
            steps_dataframe.columns.to_list()
            == expected_steps_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            steps_dataframe, expected_steps_dataframe, check_dtype=True
        )
