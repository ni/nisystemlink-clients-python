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
            workspace=uuid.uuid1().hex,
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
            properties={"Comments": "comma separated", "input": "voltage"},
        ),
    ]

    return specs


@pytest.mark.enterprise
@pytest.mark.unit
class TestSpecDataframeUtilities:
    def test__convert_specs_to_dataframe__returns_specs_dataframe(self, specs):
        conditions_dict = [
            {
                "condition_Temperature(C)": "[min: -25.0; max: 85.0; step: 20.0], 1.3, 1.5, 1.7",
                "condition_Package": "D, QFIN",
                "condition_Supply Voltage(mV)": None,
            },
            {
                "condition_Temperature(C)": "[min: -25.0; max: 85.0; step: 20.0]",
                "condition_Package": None,
                "condition_Supply Voltage(mV)": "1.3, 1.5, 1.7",
            },
            {
                "condition_Temperature(C)": None,
                "condition_Package": None,
                "condition_Supply Voltage(mV)": None,
            },
        ]
        properties_dict = [
            {
                "properties.Comments": "comma separated with unicode",
                "properties.input": None,
            },
            {"properties.Comments": None, "properties.input": None},
            {"properties.Comments": "comma separated", "properties.input": "voltage"},
        ]
        keywords_dict = [
            {"keywords": ["Test specification only", "First"]},
            {"keywords": None},
            {"keywords": None},
        ]
        expected_specs_df = self.__expected_specs_dataframe(
            specs=specs,
            conditions_dict=conditions_dict,
            properties_dict=properties_dict,
            keywords_dict=keywords_dict,
        )

        specs_df = convert_specs_to_dataframe(specs=specs)

        assert not specs_df.empty
        assert len(specs_df) == 3
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)
        assert specs_df["created_at"].dtype == "datetime64[ns, UTC]"
        assert specs_df["updated_at"].dtype == "datetime64[ns, UTC]"
        assert specs_df["type"].dtype == "object"
        assert isinstance(specs_df["type"].iloc[0], SpecificationType)
        assert specs_df["limit"].dtype == "object"
        assert isinstance(specs_df["limit"].iloc[0], SpecificationLimit)
        assert specs_df["keywords"].dtype == "object"
        assert isinstance(specs_df["keywords"].iloc[0], List)

    def test__convert_specs_to_dataframe_with_condition_format__returns_dataframe_with_specified_condition_format(
        self, specs
    ):
        def format_conditions(conditions: List[Condition]) -> Dict[str, str]:
            return {
                str(condition.name): str(condition.value.discrete)
                for condition in conditions
                if condition.value and condition.value.discrete
            }

        conditions_dict = [
            {
                "Temperature": "[1.3, 1.5, 1.7]",
                "Package": "['D', 'QFIN']",
                "Supply Voltage": None,
            },
            {
                "Temperature": None,
                "Package": None,
                "Supply Voltage": "[1.3, 1.5, 1.7]",
            },
            {
                "Temperature": None,
                "Package": None,
                "Supply Voltage(mV)": None,
            },
        ]
        properties_dict = [
            {
                "properties.Comments": "comma separated with unicode",
                "properties.input": None,
            },
            {"properties.Comments": None, "properties.input": None},
            {"properties.Comments": "comma separated", "properties.input": "voltage"},
        ]
        keywords_dict = [
            {"keywords": ["Test specification only", "First"]},
            {"keywords": None},
            {"keywords": None},
        ]
        expected_specs_df = self.__expected_specs_dataframe(
            specs=specs,
            conditions_dict=conditions_dict,
            properties_dict=properties_dict,
            keywords_dict=keywords_dict,
        )

        specs_df = convert_specs_to_dataframe(
            specs=specs,
            condition_format=format_conditions,
        )

        assert not specs_df.empty
        assert len(specs_df) == 3
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)
        assert specs_df["created_at"].dtype == "datetime64[ns, UTC]"
        assert specs_df["updated_at"].dtype == "datetime64[ns, UTC]"
        assert specs_df["type"].dtype == "object"
        assert isinstance(specs_df["type"].iloc[0], SpecificationType)
        assert specs_df["limit"].dtype == "object"
        assert isinstance(specs_df["limit"].iloc[0], SpecificationLimit)
        assert specs_df["keywords"].dtype == "object"
        assert isinstance(specs_df["keywords"].iloc[0], List)

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
        expected_specs_df = self.__expected_specs_dataframe(specs=specs)

        specs_df = convert_specs_to_dataframe(specs=specs)

        assert not specs_df.empty
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)

    def __expected_specs_dataframe(
        self, specs, conditions_dict=None, properties_dict=None, keywords_dict=None
    ):
        specs_dict = []
        index = 0
        for spec in specs:
            specs_dict.append(
                {
                    **{
                        "product_id": spec.product_id,
                        "spec_id": spec.spec_id,
                        "name": spec.name,
                        "category": spec.category,
                        "type": spec.type,
                        "symbol": spec.symbol,
                        "block": spec.block,
                        "limit": spec.limit,
                        "unit": spec.unit,
                        "workspace": spec.workspace,
                        "id": spec.id,
                        "created_at": spec.created_at,
                        "created_by": spec.created_by,
                        "updated_at": spec.updated_at,
                        "updated_by": spec.updated_by,
                        "version": spec.version,
                    },
                    **(conditions_dict[index] if conditions_dict else {}),
                    **(keywords_dict[index] if conditions_dict else {}),
                    **(properties_dict[index] if conditions_dict else {}),
                }
            )
            index += 1
        expected_specs_df = pd.DataFrame(specs_dict)
        expected_specs_df.dropna(axis="columns", how="all", inplace=True)

        return expected_specs_df
