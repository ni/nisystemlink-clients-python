import uuid
from typing import Dict, List

import pandas as pd
import pytest
from nisystemlink.clients.spec.models._condition import (
    Condition,
    ConditionRange,
    ConditionType,
    NumericConditionValue,
    StringConditionValue,
)
from nisystemlink.clients.spec.models._specification import (
    Specification,
    SpecificationLimit,
    SpecificationType,
)
from nisystemlink.clients.spec.utilities import convert_specs_to_dataframe


@pytest.fixture(scope="class")
def specs() -> List[Specification]:
    """Sample specs for this test run."""
    specs = [
        Specification(
            product_id=uuid.uuid1().hex,
            spec_id=uuid.uuid1().hex,
            name="Output voltage",
            category="Parametric Specs",
            type=SpecificationType.PARAMETRIC,
            symbol="Range",
            block="Amplifier",
            limit=SpecificationLimit(min=1.2, max=1.5, typical=1.4),
            unit="mV",
            conditions=[
                Condition(
                    name="Temperature",
                    value=NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[ConditionRange(min=-25, step=20, max=85)],
                        discrete=[1.3, 1.5, 1.7],
                        unit="C",
                    ),
                ),
                Condition(
                    name="Package",
                    value=StringConditionValue(
                        condition_type=ConditionType.STRING,
                        discrete=["D", "QFIN"],
                    ),
                ),
            ],
            keywords=["Test specification only", "First"],
            properties={"Comments": "comma separated with unicode"},
            workspace="846e294a-a007-47ac-9fc2-fac07eab240e",
            id=uuid.uuid1().hex,
            created_at="2024-03-28T13:59:12.744Z",
            created_by=uuid.uuid1().hex,
            updated_at="2024-03-28T13:59:12.744Z",
            updated_by=uuid.uuid1().hex,
            version=28,
        ),
        Specification(
            product_id=uuid.uuid1().hex,
            spec_id=uuid.uuid1().hex,
            name="Input referred voltage noise vs freq",
            category="Parametric Specs",
            type=SpecificationType.PARAMETRIC,
            symbol="Range",
            block="Amplifier",
            limit=SpecificationLimit(min=1.2, max=1.5),
            unit="mV",
            conditions=[
                Condition(
                    name="Temperature",
                    value=NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[ConditionRange(min=-25, step=20, max=85)],
                        unit="C",
                    ),
                ),
                Condition(
                    name="Supply Voltage",
                    value=NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        discrete=[1.3, 1.5, 1.7],
                        unit="mV",
                    ),
                ),
            ],
        ),
        Specification(
            product_id=uuid.uuid1().hex,
            spec_id=uuid.uuid1().hex,
            name="Input referred voltage noise vs freq",
            category="Parametric Specs",
            type=SpecificationType.PARAMETRIC,
            symbol="Range with required value",
            block="Amplifier",
            limit=SpecificationLimit(min=1.2, max=1.5),
            unit="mV",
        ),
    ]

    return specs


@pytest.fixture
def expected_specs_dataframe(specs) -> pd.DataFrame:
    """Fixture to return expected dataframe based on sample specs."""
    specs_dict = []
    for spec in specs:
        specs_dict.append(
            {
                key: value
                for key, value in vars(spec).items()
                if key not in ["conditions"]
            }
        )
    expected_specs_df = pd.json_normalize(specs_dict)

    return expected_specs_df


@pytest.mark.enterprise
@pytest.mark.unit
class TestSpecDataframeUtilities:
    def test__convert_specs_to_dataframe__returns_specs_dataframe(
        self, specs, expected_specs_dataframe
    ):
        expected_specs_df = expected_specs_dataframe
        expected_specs_df.dropna(axis="columns", how="all", inplace=True)
        properties_count = len(
            [
                column
                for column in expected_specs_df.columns.to_list()
                if column.startswith("properties.")
            ]
        )
        keywords_column = expected_specs_df.pop("keywords")
        expected_specs_df.insert(
            loc=len(expected_specs_df.columns) - properties_count,
            column="keywords",
            value=keywords_column,
        )

        specs_df = convert_specs_to_dataframe(specs=specs)
        specs_df = specs_df.drop(
            columns=[
                "condition_Temperature(C)",
                "condition_Supply Voltage(mV)",
                "condition_Package",
            ]
        )

        assert not specs_df.empty
        assert len(specs_df) == 3
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)

    def test__convert_specs_to_dataframe_without_condition_format__returns_dataframe_with_default_condition_format(
        self, specs
    ):
        expected_specs_conditions = {
            "condition_Temperature(C)": [
                "[min: -25.0; max: 85.0; step: 20.0], 1.3, 1.5, 1.7",
                "[min: -25.0; max: 85.0; step: 20.0]",
            ],
            "condition_Package": "D, QFIN",
            "condition_Supply Voltage(mV)": "1.3, 1.5, 1.7",
        }

        specs_df = convert_specs_to_dataframe(specs=specs)
        specs_df_values = specs_df.to_dict()

        assert not specs_df.empty
        assert len(specs_df) == 3
        assert (
            specs_df_values["condition_Temperature(C)"][0]
            == expected_specs_conditions["condition_Temperature(C)"][0]
        )
        assert (
            specs_df_values["condition_Temperature(C)"][1]
            == expected_specs_conditions["condition_Temperature(C)"][1]
        )
        assert pd.isna(specs_df_values["condition_Temperature(C)"][2])
        assert (
            specs_df_values["condition_Package"][0]
            == expected_specs_conditions["condition_Package"]
        )
        assert pd.isna(specs_df_values["condition_Package"][1])
        assert pd.isna(specs_df_values["condition_Package"][2])
        assert pd.isna(specs_df_values["condition_Supply Voltage(mV)"][0])
        assert (
            specs_df_values["condition_Supply Voltage(mV)"][1]
            == expected_specs_conditions["condition_Supply Voltage(mV)"]
        )
        assert pd.isna(specs_df_values["condition_Supply Voltage(mV)"][2])

    def test__convert_specs_to_dataframe_with_condition_format__returns_dataframe_with_specified_condition_format(
        self, specs
    ):
        def format_conditions(conditions: List[Condition]) -> Dict[str, str]:
            return {
                str(condition.name): str(condition.value.discrete)
                for condition in conditions
                if condition.value and condition.value.discrete
            }

        expected_specs_conditions = {
            "Temperature": "[1.3, 1.5, 1.7]",
            "Package": "['D', 'QFIN']",
            "Supply Voltage": "[1.3, 1.5, 1.7]",
        }

        specs_df = convert_specs_to_dataframe(
            specs=specs,
            condition_format=format_conditions,
        )

        assert not specs_df.empty
        assert len(specs_df) == 3
        assert specs_df["Temperature"][0] == expected_specs_conditions["Temperature"]
        assert pd.isna(specs_df["Temperature"][1])
        assert pd.isna(specs_df["Temperature"][2])
        assert specs_df["Package"][0] == expected_specs_conditions["Package"]
        assert pd.isna(specs_df["Package"][1])
        assert pd.isna(specs_df["Package"][2])
        assert pd.isna(specs_df["Supply Voltage"][0])
        assert (
            specs_df["Supply Voltage"][1] == expected_specs_conditions["Supply Voltage"]
        )
        assert pd.isna(specs_df["Supply Voltage"][2])

    def test__convert_specs_to_dataframe_without_condition_values__returns_specs_dataframe_without_condition(
        self,
    ):
        specs = [
            Specification(
                product_id=uuid.uuid1().hex,
                spec_id=uuid.uuid1().hex,
                name="Input referred voltage noise vs freq",
                conditions=[
                    Condition(
                        name="Temperature",
                    ),
                    Condition(
                        name="Supply Voltage",
                    ),
                ],
            ),
        ]
        expected_specs_columns = [
            "product_id",
            "spec_id",
            "name",
        ]
        expected_specs_dict = {
            "product_id": specs[0].product_id,
            "spec_id": specs[0].spec_id,
            "name": specs[0].name,
        }
        expected_specs_df = pd.DataFrame(expected_specs_dict, index=[0])

        specs_df = convert_specs_to_dataframe(specs=specs)
        specs_columns = specs_df.columns.to_list()

        assert not specs_df.empty
        assert specs_columns == expected_specs_columns
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)
