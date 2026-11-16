import uuid
from datetime import datetime, timezone
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
    MeasurementMappingItem,
    Specification,
    SpecificationLimit,
    SpecificationType,
)
from nisystemlink.clients.spec.utilities import convert_specs_to_dataframe
from nisystemlink.clients.spec.utilities._dataframe_utilities import (
    normalize_conditions_per_column,
    normalize_conditions_per_row,
    normalize_measurement_mappings_per_column,
    normalize_measurement_mappings_per_row,
    summarize_conditions_as_a_string,
    summarize_measurement_mappings_as_a_string,
)

# Python datetime fixtures infer nanoseconds in pandas 2 and microseconds in pandas 3.
DATETIME_DTYPE = (
    "datetime64[ns, UTC]" if pd.__version__.startswith("2.") else "datetime64[us, UTC]"
)


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
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                        ],
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
            measurement_mapping=[
                MeasurementMappingItem(
                    filter='data.parameters.Any(it["name"] == "Output Voltage")',
                    result_filter='partNumber == "VR1234"',
                ),
                MeasurementMappingItem(
                    filter='data.parameters.Any(it["name"] == "Input Voltage")',
                    result_filter='partNumber == "VR5678"',
                ),
            ],
            workspace=uuid.uuid1().hex,
            id=uuid.uuid1().hex,
            created_at=datetime(2024, 3, 28, 13, 59, 12, 744000, tzinfo=timezone.utc),
            created_by=uuid.uuid1().hex,
            updated_at=datetime(2024, 3, 28, 13, 59, 12, 744000, tzinfo=timezone.utc),
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
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                            ConditionRange(min=-10, step=10),
                        ],
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
            measurement_mapping=[
                MeasurementMappingItem(result_filter='programName == "Production Test"')
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


@pytest.mark.unit
class TestSpecDataframeUtilities:
    def test__convert_specs_to_dataframe_with_summarize_conditions__returns_specs_dataframe_with_string_conditions(
        self, specs
    ):
        conditions_dict = [
            [
                {
                    "condition_Temperature(C)": "[min: -25.0; max: 85.0; step: 20.0], 1.3, 1.5, 1.7",
                    "condition_Package": "D, QFIN",
                    "condition_Supply Voltage(mV)": None,
                }
            ],
            [
                {
                    "condition_Temperature(C)": "[min: -25.0; max: 85.0; step: 20.0], [min: -10.0; step: 10.0]",
                    "condition_Package": None,
                    "condition_Supply Voltage(mV)": "1.3, 1.5, 1.7",
                }
            ],
            [
                {
                    "condition_Temperature(C)": None,
                    "condition_Package": None,
                    "condition_Supply Voltage(mV)": None,
                }
            ],
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
            specs=specs, condition_format=summarize_conditions_as_a_string
        )

        assert not specs_df.empty
        assert len(specs_df) == 3
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)
        assert specs_df["created_at"].dtype == DATETIME_DTYPE
        assert specs_df["updated_at"].dtype == DATETIME_DTYPE
        assert specs_df["keywords"].dtype == "object"
        assert isinstance(specs_df["keywords"].iloc[0], List)

    def test__convert_specs_to_dataframe_with_condition_format__returns_dataframe_with_specified_condition_format(
        self, specs
    ):
        def format_conditions(conditions: List[Condition]) -> List[Dict[str, str]]:
            return [
                {
                    str(condition.name): str(condition.value.discrete)
                    for condition in conditions
                    if condition.value and condition.value.discrete
                }
            ]

        conditions_dict = [
            [
                {
                    "Temperature": "[1.3, 1.5, 1.7]",
                    "Package": "['D', 'QFIN']",
                    "Supply Voltage": None,
                }
            ],
            [
                {
                    "Temperature": None,
                    "Package": None,
                    "Supply Voltage": "[1.3, 1.5, 1.7]",
                }
            ],
            [
                {
                    "Temperature": None,
                    "Package": None,
                    "Supply Voltage(mV)": None,
                }
            ],
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
        assert specs_df["created_at"].dtype == DATETIME_DTYPE
        assert specs_df["updated_at"].dtype == DATETIME_DTYPE
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

    @pytest.mark.parametrize(
        "mapping, expected_mapping_columns",
        [
            (None, []),
            ([], []),
            ([MeasurementMappingItem()], []),
            (
                [MeasurementMappingItem(filter='name == "Output Voltage"')],
                ["measurement_mapping[0].filter"],
            ),
            (
                [MeasurementMappingItem(result_filter='partNumber == "VR1234"')],
                ["measurement_mapping[0].result_filter"],
            ),
            (
                [MeasurementMappingItem(filter="", result_filter="")],
                [
                    "measurement_mapping[0].filter",
                    "measurement_mapping[0].result_filter",
                ],
            ),
            (
                [
                    MeasurementMappingItem(filter='name == "Output Voltage"'),
                    MeasurementMappingItem(filter='name == "Input Voltage"'),
                ],
                ["measurement_mapping[0].filter", "measurement_mapping[1].filter"],
            ),
        ],
        ids=[
            "none",
            "empty_list",
            "empty_item",
            "filter_only",
            "result_filter_only",
            "empty_strings_are_kept",
            "multiple_items",
        ],
    )
    def test__convert_specs_to_dataframe_with_empty_or_partial_measurement_mapping__returns_expected_mapping_columns(
        self, mapping, expected_mapping_columns
    ):
        specs = [
            Specification(
                product_id=uuid.uuid1().hex,
                spec_id=uuid.uuid1().hex,
                name="Output voltage",
                measurement_mapping=mapping,
            ),
        ]
        expected_specs_df = self.__expected_specs_dataframe(specs=specs)

        specs_df = convert_specs_to_dataframe(specs=specs)

        mapping_columns = [
            c for c in specs_df.columns if c.startswith("measurement_mapping")
        ]
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)

    def test__convert_specs_to_dataframe_with_measurement_mapping_per_row__returns_row_per_mapping(
        self,
    ):
        specs = [
            Specification(
                spec_id="S1",
                measurement_mapping=[
                    MeasurementMappingItem(filter="F1", result_filter="R1"),
                    MeasurementMappingItem(filter="F2"),
                ],
            ),
            Specification(spec_id="S2"),
        ]

        specs_df = convert_specs_to_dataframe(
            specs=specs,
            measurement_mapping_format=normalize_measurement_mappings_per_row,
        )

        assert specs_df["spec_id"].to_list() == ["S1", "S1", "S2"]
        assert specs_df["measurement_mapping.filter"].to_list()[:2] == ["F1", "F2"]
        assert specs_df["measurement_mapping.result_filter"].iloc[0] == "R1"
        assert pd.isna(specs_df["measurement_mapping.result_filter"].iloc[1])
        assert pd.isna(specs_df["measurement_mapping.filter"].iloc[2])

    def test__convert_specs_to_dataframe_with_measurement_mapping_summary__returns_string_summary(
        self,
    ):
        specs = [
            Specification(
                spec_id="S1",
                measurement_mapping=[
                    MeasurementMappingItem(filter="F1", result_filter="R1"),
                    MeasurementMappingItem(filter="F2"),
                ],
            ),
        ]

        specs_df = convert_specs_to_dataframe(
            specs=specs,
            measurement_mapping_format=summarize_measurement_mappings_as_a_string,
        )

        assert len(specs_df) == 1
        assert (
            specs_df["measurement_mapping"].iloc[0]
            == "[filter: F1; result_filter: R1], [filter: F2]"
        )

    def test__convert_specs_to_dataframe_when_measurement_mapping_format_none__returns_dataframe_without_mapping(
        self,
    ):
        specs = [
            Specification(
                spec_id="S1",
                measurement_mapping=[MeasurementMappingItem(filter="F1")],
            ),
        ]

        specs_df = convert_specs_to_dataframe(
            specs=specs, measurement_mapping_format=None
        )

        assert len(specs_df) == 1
        assert not [c for c in specs_df.columns if c.startswith("measurement_mapping")]

    def test__convert_specs_to_dataframe_with_custom_measurement_mapping_format__uses_custom_format(
        self,
    ):
        specs = [
            Specification(
                spec_id="S1",
                measurement_mapping=[
                    MeasurementMappingItem(filter="F1"),
                    MeasurementMappingItem(filter="F2"),
                ],
            ),
        ]

        specs_df = convert_specs_to_dataframe(
            specs=specs,
            measurement_mapping_format=lambda items: [
                {"mapped_filters": [item.filter for item in items]}
            ],
        )

        assert specs_df["mapped_filters"].iloc[0] == ["F1", "F2"]

    def test__normalize_measurement_mappings__returns_expected_formats(self):
        mappings = [
            MeasurementMappingItem(filter="F1", result_filter="R1"),
            MeasurementMappingItem(),
            MeasurementMappingItem(result_filter="R3"),
        ]

        assert normalize_measurement_mappings_per_column(mappings) == [
            {
                "measurement_mapping[0].filter": "F1",
                "measurement_mapping[0].result_filter": "R1",
                "measurement_mapping[2].result_filter": "R3",
            }
        ]
        assert normalize_measurement_mappings_per_row(mappings) == [
            {
                "measurement_mapping.filter": "F1",
                "measurement_mapping.result_filter": "R1",
            },
            {"measurement_mapping.result_filter": "R3"},
        ]
        assert summarize_measurement_mappings_as_a_string(mappings) == [
            {
                "measurement_mapping": "[filter: F1; result_filter: R1], [result_filter: R3]"
            }
        ]
        assert normalize_measurement_mappings_per_column([]) == []

    def test__convert_specs_to_dataframe_with_condition_per_column__returns_dataframe_with_condition_per_column(
        self, specs
    ):
        conditions_dict = [
            [
                {
                    "condition_Temperature": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                        ],
                        discrete=[1.3, 1.5, 1.7],
                        unit="C",
                    ),
                    "condition_Package": StringConditionValue(
                        condition_type=ConditionType.STRING,
                        discrete=["D", "QFIN"],
                    ),
                    "condition_Supply Voltage": None,
                }
            ],
            [
                {
                    "condition_Temperature": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                            ConditionRange(min=-10, step=10),
                        ],
                        unit="C",
                    ),
                    "condition_Package": None,
                    "condition_Supply Voltage": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        discrete=[1.3, 1.5, 1.7],
                        unit="mV",
                    ),
                }
            ],
            [
                {
                    "condition_Temperature": None,
                    "condition_Package": None,
                    "condition_Supply Voltage(mV)": None,
                }
            ],
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
            specs=specs, condition_format=normalize_conditions_per_column
        )

        assert not specs_df.empty
        assert len(specs_df) == 3
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)
        assert specs_df["created_at"].dtype == DATETIME_DTYPE
        assert specs_df["updated_at"].dtype == DATETIME_DTYPE
        assert specs_df["keywords"].dtype == "object"
        assert isinstance(specs_df["keywords"].iloc[0], List)

    def test__convert_specs_to_dataframe_with_condition_per_row__returns_dataframe_with_condition_per_row(
        self, specs
    ):
        conditions_dict = [
            [
                {
                    "condition.name": "Temperature",
                    "condition.value": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                        ],
                        discrete=[1.3, 1.5, 1.7],
                        unit="C",
                    ),
                },
                {
                    "condition.name": "Package",
                    "condition.value": StringConditionValue(
                        condition_type=ConditionType.STRING,
                        discrete=["D", "QFIN"],
                    ),
                },
            ],
            [
                {
                    "condition.name": "Temperature",
                    "condition.value": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                            ConditionRange(min=-10, step=10),
                        ],
                        unit="C",
                    ),
                },
                {
                    "condition.name": "Supply Voltage",
                    "condition.value": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        discrete=[1.3, 1.5, 1.7],
                        unit="mV",
                    ),
                },
            ],
            [],
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
            specs=specs, condition_format=normalize_conditions_per_row
        )

        assert not specs_df.empty
        assert len(specs_df) == 5
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)
        assert specs_df["created_at"].dtype == DATETIME_DTYPE
        assert specs_df["updated_at"].dtype == DATETIME_DTYPE
        assert specs_df["keywords"].dtype == "object"
        assert isinstance(specs_df["keywords"].iloc[0], List)

    def test__convert_specs_to_dataframe_when_condition_format_none__returns_dataframe_without_condition(
        self, specs
    ):
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
            specs=specs, properties_dict=properties_dict, keywords_dict=keywords_dict
        )

        specs_df = convert_specs_to_dataframe(specs=specs, condition_format=None)

        assert not specs_df.empty
        assert len(specs_df) == 3
        pd.testing.assert_frame_equal(specs_df, expected_specs_df, check_dtype=True)
        assert specs_df["created_at"].dtype == DATETIME_DTYPE
        assert specs_df["updated_at"].dtype == DATETIME_DTYPE
        assert specs_df["keywords"].dtype == "object"
        assert isinstance(specs_df["keywords"].iloc[0], List)

    def test__summarize_conditions_to_string__returns_only_conditions_with_value_in_string_format(
        self, specs
    ):
        expected_conditions_dict = [
            [
                {
                    "condition_Temperature(C)": "[min: -25.0; max: 85.0; step: 20.0], 1.3, 1.5, 1.7",
                    "condition_Package": "D, QFIN",
                }
            ],
            [
                {
                    "condition_Temperature(C)": "[min: -25.0; max: 85.0; step: 20.0], [min: -10.0; step: 10.0]",
                    "condition_Supply Voltage(mV)": "1.3, 1.5, 1.7",
                }
            ],
        ]

        conditions_dict = [
            summarize_conditions_as_a_string(spec.conditions)
            for spec in specs
            if spec.conditions
        ]

        assert conditions_dict == expected_conditions_dict

    def test__normalize_conditions_per_column__returns_only_conditions_in_conditions_per_column_format(
        self, specs
    ):
        expected_conditions_dict = [
            [
                {
                    "condition_Temperature": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                        ],
                        discrete=[1.3, 1.5, 1.7],
                        unit="C",
                    ),
                    "condition_Package": StringConditionValue(
                        condition_type=ConditionType.STRING,
                        discrete=["D", "QFIN"],
                    ),
                }
            ],
            [
                {
                    "condition_Temperature": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                            ConditionRange(min=-10, step=10),
                        ],
                        unit="C",
                    ),
                    "condition_Supply Voltage": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        discrete=[1.3, 1.5, 1.7],
                        unit="mV",
                    ),
                }
            ],
        ]

        conditions_dict = [
            normalize_conditions_per_column(spec.conditions)
            for spec in specs
            if spec.conditions
        ]

        assert conditions_dict == expected_conditions_dict

    def test__normalize_conditions_per_row__returns_only_conditions_in_conditions_per_row_format(
        self, specs
    ):
        expected_conditions_dict = [
            [
                {
                    "condition.name": "Temperature",
                    "condition.value": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                        ],
                        discrete=[1.3, 1.5, 1.7],
                        unit="C",
                    ),
                },
                {
                    "condition.name": "Package",
                    "condition.value": StringConditionValue(
                        condition_type=ConditionType.STRING,
                        discrete=["D", "QFIN"],
                    ),
                },
            ],
            [
                {
                    "condition.name": "Temperature",
                    "condition.value": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        range=[
                            ConditionRange(min=-25, step=20, max=85),
                            ConditionRange(min=-10, step=10),
                        ],
                        unit="C",
                    ),
                },
                {
                    "condition.name": "Supply Voltage",
                    "condition.value": NumericConditionValue(
                        condition_type=ConditionType.NUMERIC,
                        discrete=[1.3, 1.5, 1.7],
                        unit="mV",
                    ),
                },
            ],
        ]

        conditions_dict = [
            normalize_conditions_per_row(spec.conditions)
            for spec in specs
            if spec.conditions
        ]

        assert conditions_dict == expected_conditions_dict

    def __expected_specs_dataframe(
        self, specs, conditions_dict=None, keywords_dict=None, properties_dict=None
    ):
        specs_dict = []
        index = 0
        for spec in specs:
            for condition in (
                conditions_dict[index]
                if (conditions_dict and conditions_dict[index])
                else [{}]
            ):
                specs_dict.append(
                    {
                        **{
                            "product_id": spec.product_id,
                            "spec_id": spec.spec_id,
                            "name": spec.name,
                            "category": spec.category,
                            "symbol": spec.symbol,
                            "block": spec.block,
                            "unit": spec.unit,
                            "workspace": spec.workspace,
                            "id": spec.id,
                            "created_at": spec.created_at,
                            "created_by": spec.created_by,
                            "updated_at": spec.updated_at,
                            "updated_by": spec.updated_by,
                            "version": spec.version,
                            "type": spec.type.name if spec.type else None,
                            "limit.min": spec.limit.min if spec.limit else None,
                            "limit.typical": spec.limit.typical if spec.limit else None,
                            "limit.max": spec.limit.max if spec.limit else None,
                            **{
                                f"measurement_mapping[{mapping_index}].{key}": value
                                for mapping_index, mapping in enumerate(
                                    spec.measurement_mapping or []
                                )
                                for key, value in (
                                    ("filter", mapping.filter),
                                    ("result_filter", mapping.result_filter),
                                )
                                if value is not None
                            },
                        },
                        **{
                            key: float("nan") if value is None else value
                            for key, value in condition.items()
                        },
                        **(keywords_dict[index] if keywords_dict else {}),
                        **(properties_dict[index] if properties_dict else {}),
                    }
                )
            index += 1
        expected_specs_df = pd.DataFrame(specs_dict)
        expected_specs_df.dropna(axis="columns", how="all", inplace=True)

        return expected_specs_df
