import datetime
import uuid
from typing import List

import pandas as pd
import pytest
from nisystemlink.clients.testmonitor.models import (
    Measurement,
    NamedValue,
    Result,
    Status,
    StatusType,
    Step,
    StepData,
)
from nisystemlink.clients.testmonitor.utilities._dataframe_utilities import (
    convert_results_to_dataframe,
    convert_steps_to_dataframe,
)


@pytest.fixture(scope="class")
def results() -> List[Result]:
    """Sample results for testing purposes."""
    results = [
        Result(
            status=Status.PASSED(),
            started_at=datetime.datetime(
                2018, 5, 7, 18, 58, 5, 219692, tzinfo=datetime.timezone.utc
            ),
            updated_at=datetime.datetime(
                2018, 5, 7, 18, 58, 5, 219692, tzinfo=datetime.timezone.utc
            ),
            program_name="My Program Name",
            id=uuid.uuid1().hex,
            system_id=uuid.uuid1().hex,
            host_name="host name",
            part_number=uuid.uuid1().hex,
            serial_number=uuid.uuid1().hex,
            total_time_in_seconds=16.76845106446358,
            keywords=["keyword1", "keyword2"],
            properties={"property1": "value1", "property2": "value2"},
            operator="sample operator",
            file_ids=[uuid.uuid1().hex, uuid.uuid1().hex],
            data_table_ids=[uuid.uuid1().hex, uuid.uuid1().hex],
            status_type_summary={StatusType.PASSED: 1, StatusType.FAILED: 0},
            workspace=uuid.uuid1().hex,
        ),
        Result(
            status=Status.FAILED(),
            started_at=datetime.datetime(
                2018, 5, 7, 18, 58, 5, 219692, tzinfo=datetime.timezone.utc
            ),
            updated_at=datetime.datetime(
                2018, 5, 7, 18, 58, 5, 219692, tzinfo=datetime.timezone.utc
            ),
            program_name="My Program Name",
            id=uuid.uuid1().hex,
            part_number=uuid.uuid1().hex,
            total_time_in_seconds=16.76845106446358,
            keywords=[],
            properties={"property3": "value3"},
            file_ids=[uuid.uuid1().hex],
            status_type_summary={StatusType.PASSED: 0, StatusType.FAILED: 1},
            workspace=uuid.uuid1().hex,
        ),
        Result(
            status=Status(status_type=StatusType.CUSTOM, status_name="custom_status"),
            started_at=datetime.datetime(
                2018, 5, 7, 18, 58, 5, 219692, tzinfo=datetime.timezone.utc
            ),
            updated_at=datetime.datetime(
                2018, 5, 7, 18, 58, 5, 219692, tzinfo=datetime.timezone.utc
            ),
            program_name="My Program Name",
            id=uuid.uuid1().hex,
            file_ids=[uuid.uuid1().hex],
            status_type_summary={StatusType.PASSED: 0, StatusType.FAILED: 1},
            workspace=uuid.uuid1().hex,
        ),
    ]

    return results


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
        started_at=datetime.datetime(
            2023, 3, 27, 18, 39, 49, tzinfo=datetime.timezone.utc
        ),
        updated_at=datetime.datetime(
            2024, 2, 2, 14, 22, 4, 625155, tzinfo=datetime.timezone.utc
        ),
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
                Measurement(
                    name="parameter_11",
                    units="A",
                    status="Passed",
                    lowLimit="6.0",
                    highLimit="21.0",
                    measurement="11.0",
                    comparisonType="GTLT",
                ),
                Measurement(additionalProp="myValue"),
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
        status=Status(status_type=StatusType.CUSTOM, status_name="newstatus"),
        total_time_in_seconds=5,
        started_at=datetime.datetime(
            2023, 3, 27, 18, 39, 49, tzinfo=datetime.timezone.utc
        ),
        updated_at=datetime.datetime(
            2024, 2, 2, 14, 22, 4, 625255, tzinfo=datetime.timezone.utc
        ),
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
                Measurement(
                    name="parameter_21",
                    units="A",
                    status="Passed",
                    lowLimit="6.0",
                    highLimit="21.0",
                    measurement="11.0",
                    comparisonType="GTLT",
                    additionalData="additional_data_value",
                ),
                Measurement(
                    name="parameter_22",
                    units="C",
                    status="Passed",
                    lowLimit="7.0",
                    highLimit="22.0",
                    comparisonType="GTLT",
                ),
            ],
        ),
        has_children=True,
        workspace="846e294a-a007-47ac-9fc2-fac07eab240z",
        keywords=["keyword21", "keyword22"],
        properties={"property21": "property21_value", "property22": "property22_value"},
    )
    return [step1, step2]


@pytest.fixture
def empty_steps_data() -> List:
    """Fixture to return an empty list of steps."""
    return []


@pytest.mark.enterprise
@pytest.mark.unit
class TestTestmonitorDataframeUtilities:
    def test__convert_results_with_all_fields_to_dataframe__returns_whole_results_dataframe(
        self, results
    ):
        expected_results_dataframe = self.__get_expected_results_dataframe(
            results=results
        )

        results_dataframe = convert_results_to_dataframe(
            results=results, set_id_as_index=False
        )

        assert not results_dataframe.empty
        assert len(results_dataframe.columns.tolist()) == 20
        pd.testing.assert_frame_equal(
            results_dataframe, expected_results_dataframe, check_dtype=True
        )
        assert isinstance(results_dataframe["status"].iloc[0], str)
        assert results_dataframe["started_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["updated_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["file_ids"].dtype == "object"
        assert isinstance(results_dataframe["file_ids"].iloc[0], List)
        assert results_dataframe["data_table_ids"].dtype == "object"
        assert isinstance(results_dataframe["data_table_ids"].iloc[0], List)
        assert results_dataframe["keywords"].dtype == "object"
        assert isinstance(results_dataframe["keywords"].iloc[0], List)

    def test__convert_results_with_specific_fields_to_dataframe__returns_results_dataframe_with_specific_fields(
        self, results
    ):
        results = results[1:]
        expected_results_dataframe = self.__get_expected_results_dataframe(
            results=results
        )

        results_dataframe = convert_results_to_dataframe(
            results=results, set_id_as_index=False
        )

        assert not results_dataframe.empty
        assert len(results_dataframe.columns.tolist()) == 13
        pd.testing.assert_frame_equal(
            results_dataframe, expected_results_dataframe, check_dtype=True
        )
        assert isinstance(results_dataframe["status"].iloc[0], str)
        assert results_dataframe["started_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["updated_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["file_ids"].dtype == "object"
        assert isinstance(results_dataframe["file_ids"].iloc[0], List)
        assert results_dataframe["keywords"].dtype == "object"
        assert isinstance(results_dataframe["keywords"].iloc[0], List)

    def test__convert_results_to_dataframe_with_id_index__returns_results_dataframe_with_id_index(
        self, results
    ):
        expected_results_dataframe = self.__get_expected_results_dataframe(
            results=results
        )
        expected_results_dataframe = expected_results_dataframe.set_index("id")

        results_dataframe = convert_results_to_dataframe(results=results)

        assert not results_dataframe.empty
        assert len(results_dataframe.columns.tolist()) == 19
        pd.testing.assert_frame_equal(
            results_dataframe, expected_results_dataframe, check_dtype=True
        )
        assert isinstance(results_dataframe["status"].iloc[0], str)
        assert results_dataframe["started_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["updated_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["file_ids"].dtype == "object"
        assert isinstance(results_dataframe["file_ids"].iloc[0], List)
        assert results_dataframe["data_table_ids"].dtype == "object"
        assert isinstance(results_dataframe["data_table_ids"].iloc[0], List)
        assert results_dataframe["keywords"].dtype == "object"
        assert isinstance(results_dataframe["keywords"].iloc[0], List)

    def test__convert_results_to_dataframe_with_no_results__returns_empty_dataframe(
        self,
    ):
        results_dataframe = convert_results_to_dataframe(results=[])

        assert isinstance(results_dataframe, pd.DataFrame)
        assert results_dataframe.empty

    def test__convert_steps_to_dataframe__with_complete_data(
        self, mock_steps_data: List[Step]
    ):
        """Test normal case with valid step data."""
        expected_data_parameters = [
            [
                {
                    "data.measurement.name": "parameter_11",
                    "data.measurement.status": "Passed",
                    "data.measurement.measurement": "11.0",
                    "data.measurement.lowLimit": "6.0",
                    "data.measurement.highLimit": "21.0",
                    "data.measurement.units": "A",
                    "data.measurement.comparisonType": "GTLT",
                }
            ],
            [
                {
                    "data.measurement.name": "parameter_21",
                    "data.measurement.status": "Passed",
                    "data.measurement.measurement": "11.0",
                    "data.measurement.lowLimit": "6.0",
                    "data.measurement.highLimit": "21.0",
                    "data.measurement.units": "A",
                    "data.measurement.comparisonType": "GTLT",
                    "data.measurement.additionalData": "additional_data_value",
                }
            ],
        ]
        expected_steps_dataframe = self.__get_expected_steps_dataframe(
            mock_steps_data, expected_data_parameters
        )

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
        self, mock_steps_data: List[Step]
    ):
        """Test case when some fields in step data are missing."""
        expected_steps_dataframe = self.__get_expected_steps_dataframe(mock_steps_data)
        steps = mock_steps_data
        for step in steps:
            step.path_ids = None
            step.data = None
            step.inputs = None
        expected_steps_dataframe = expected_steps_dataframe.drop(
            columns=[
                "path_ids",
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
        steps_dataframe = convert_steps_to_dataframe(steps)

        assert not steps_dataframe.empty
        assert (
            steps_dataframe.columns.to_list()
            == expected_steps_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            steps_dataframe, expected_steps_dataframe, check_dtype=True
        )

    def test__convert_steps_to_dataframe_with_callback__returns_dataframe_with_valid_measurement(
        self, mock_steps_data: List[Step]
    ):
        """Test if the function returns a dataframe of steps with valid measurement."""

        def is_measurement_data_parameter(measurement: Measurement) -> bool:
            return measurement.name is not None and hasattr(
                measurement, "additionalData"
            )

        expected_data_parameters = [
            [{}],
            [
                {
                    "data.measurement.name": "parameter_21",
                    "data.measurement.status": "Passed",
                    "data.measurement.measurement": "11.0",
                    "data.measurement.lowLimit": "6.0",
                    "data.measurement.highLimit": "21.0",
                    "data.measurement.units": "A",
                    "data.measurement.comparisonType": "GTLT",
                    "data.measurement.additionalData": "additional_data_value",
                }
            ],
        ]
        expected_steps_dataframe = self.__get_expected_steps_dataframe(
            mock_steps_data, expected_data_parameters
        )

        steps_dataframe = convert_steps_to_dataframe(
            mock_steps_data, is_measurement_data_parameter
        )

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

    def test__convert_steps_to_dataframe_with_invalid_data_parameters__returns_only_step_data_without_measurement(
        self,
    ):
        """Test if the function returns a dataframe of steps with no measurement."""
        step_data = Step(
            name="step_name",
            step_id="5ffb2bf6771fa11e877838dd6",
            result_id="5ffb2bf6771fa11e877838dd8",
            data=StepData(
                text="data1",
                parameters=[Measurement(name="parameter_123", status="Passed")],
            ),
        )
        expected_column_order = [
            "name",
            "step_id",
            "result_id",
            "status",
            "data.text",
        ]
        expected_steps_dataframe = self.__get_expected_steps_dataframe(
            [step_data], expected_column_order=expected_column_order
        )

        steps_dataframe = convert_steps_to_dataframe([step_data])

        assert not steps_dataframe.empty
        assert (
            steps_dataframe.columns.to_list()
            == expected_steps_dataframe.columns.to_list()
        )
        pd.testing.assert_frame_equal(
            steps_dataframe, expected_steps_dataframe, check_dtype=True
        )

    def test__convert_steps_to_dataframe_with_none_callback__returns_step_with_all_data_parameters(
        self, mock_steps_data: List[Step]
    ):
        """Test normal case with valid step data."""
        expected_data_parameters = [
            [
                {
                    "data.parameters.name": "parameter_11",
                    "data.parameters.status": "Passed",
                    "data.parameters.measurement": "11.0",
                    "data.parameters.lowLimit": "6.0",
                    "data.parameters.highLimit": "21.0",
                    "data.parameters.units": "A",
                    "data.parameters.comparisonType": "GTLT",
                },
                {
                    "data.parameters.additionalProp": "myValue",
                },
            ],
            [
                {
                    "data.parameters.name": "parameter_21",
                    "data.parameters.status": "Passed",
                    "data.parameters.measurement": "11.0",
                    "data.parameters.lowLimit": "6.0",
                    "data.parameters.highLimit": "21.0",
                    "data.parameters.units": "A",
                    "data.parameters.comparisonType": "GTLT",
                    "data.parameters.additionalData": "additional_data_value",
                },
                {
                    "data.parameters.name": "parameter_22",
                    "data.parameters.status": "Passed",
                    "data.parameters.lowLimit": "7.0",
                    "data.parameters.highLimit": "22.0",
                    "data.parameters.units": "C",
                    "data.parameters.comparisonType": "GTLT",
                },
            ],
        ]
        expected_steps_dataframe = self.__get_expected_steps_dataframe(
            mock_steps_data,
            expected_data_parameters=expected_data_parameters,
            data_parameters_prefix="data.parameters",
        )

        steps_dataframe = convert_steps_to_dataframe(mock_steps_data, None)

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

    def __get_expected_results_dataframe(self, results: List[Result]):
        results_dict = []
        for result in results:
            status = {
                "status": (
                    result.status.status_type.value
                    if result.status and result.status.status_type != "CUSTOM"
                    else result.status.status_name if result.status else None
                )
            }
            status_type_summary = (
                {
                    f"status_type_summary.{key}": value
                    for key, value in result.status_type_summary.items()
                }
                if result.status_type_summary
                else {}
            )
            properties = (
                {f"properties.{key}": value for key, value in result.properties.items()}
                if result.properties
                else {}
            )
            results_dict.append(
                {
                    **{
                        "started_at": result.started_at,
                        "updated_at": result.updated_at,
                        "program_name": result.program_name,
                        "id": result.id,
                        "system_id": result.system_id,
                        "host_name": result.host_name,
                        "part_number": result.part_number,
                        "serial_number": result.serial_number,
                        "total_time_in_seconds": result.total_time_in_seconds,
                        "keywords": result.keywords,
                        "operator": result.operator,
                        "file_ids": result.file_ids,
                        "data_table_ids": result.data_table_ids,
                        "workspace": result.workspace,
                    },
                    **status,
                    **status_type_summary,
                    **properties,
                }
            )

        results_df = pd.DataFrame(results_dict)
        results_df = results_df[
            ["status"] + [col for col in results_df.columns if col != "status"]
        ]
        results_df.dropna(axis="columns", how="all", inplace=True)

        return results_df

    def __get_expected_steps_dataframe(
        self,
        mock_steps_data: List[Step],
        expected_data_parameters=None,
        expected_column_order=None,
        data_parameters_prefix="data.measurement",
    ) -> pd.DataFrame:
        steps_with_measurement_per_row = []
        index = 0
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
            for parameter in (
                expected_data_parameters[index]
                if (expected_data_parameters and expected_data_parameters[index])
                else [{}]
            ):
                steps_with_measurement_per_row.append(
                    {
                        "name": step.name,
                        "step_type": step.step_type,
                        "step_id": step.step_id,
                        "parent_id": step.parent_id,
                        "result_id": step.result_id,
                        "path": step.path,
                        "path_ids": step.path_ids,
                        "status": (
                            step.status.status_type.value
                            if step.status and step.status.status_type != "CUSTOM"
                            else step.status.status_name if step.status else None
                        ),
                        "total_time_in_seconds": step.total_time_in_seconds,
                        "started_at": step.started_at,
                        "updated_at": step.updated_at,
                        "data_model": step.data_model,
                        "has_children": step.has_children,
                        "workspace": step.workspace,
                        "keywords": step.keywords,
                        **inputs,
                        **outputs,
                        "data.text": step.data.text if step.data else None,
                        **{key: value for key, value in (parameter.items() or {})},
                        **properties,
                    }
                )
            index += 1

        steps_dataframe = pd.DataFrame(steps_with_measurement_per_row)

        dataframe_columns = [
            col
            for col in steps_dataframe.columns
            if col.startswith(data_parameters_prefix)
        ]
        default_column_order = [
            "name",
            "step_type",
            "step_id",
            "parent_id",
            "result_id",
            "path",
            "path_ids",
            "status",
            "total_time_in_seconds",
            "started_at",
            "updated_at",
            "data_model",
            "has_children",
            "workspace",
            "keywords",
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
            *dataframe_columns,
            "properties.property11",
            "properties.property12",
            "properties.property21",
            "properties.property22",
        ]
        return steps_dataframe.reindex(
            columns=expected_column_order or default_column_order, copy=False
        )
