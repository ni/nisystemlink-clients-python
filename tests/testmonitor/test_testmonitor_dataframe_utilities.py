import datetime
import uuid
from typing import List

import pandas as pd
import pytest
from nisystemlink.clients.testmonitor.models._result import Result
from nisystemlink.clients.testmonitor.models._status import Status, StatusType
from nisystemlink.clients.testmonitor.utilities._dataframe_utilities import (
    convert_results_to_dataframe,
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
            status=Status.FAILED(),
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


@pytest.mark.enterprise
class TestTestmonitorDataframeUtilities:
    def test__convert_results_with_all_fields_to_dataframe__returns_whole_results_dataframe(
        self, results
    ):
        expected_results_dataframe = self.get_expected_results_dataframe(
            results=results
        )
        expected_result_index = [0, 1, 2]

        results_dataframe = convert_results_to_dataframe(results=results)
        results_index = results_dataframe.index.to_list()

        assert not results_dataframe.empty
        assert isinstance(results_dataframe, pd.DataFrame)
        assert len(results_dataframe) == 3
        assert len(results_dataframe.columns.tolist()) == 20
        assert results_index == expected_result_index
        pd.testing.assert_frame_equal(
            results_dataframe, expected_results_dataframe, check_dtype=True
        )
        assert results_dataframe["status.status_type"].dtype == "object"
        assert isinstance(results_dataframe["status.status_type"].iloc[0], StatusType)
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
        expected_results_dataframe = self.get_expected_results_dataframe(
            results=results
        )
        expected_result_index = [0, 1]

        results_dataframe = convert_results_to_dataframe(results=results)
        results_index = results_dataframe.index.to_list()

        assert not results_dataframe.empty
        assert isinstance(results_dataframe, pd.DataFrame)
        assert len(results_dataframe) == 2
        assert len(results_dataframe.columns.tolist()) == 13
        assert results_index == expected_result_index
        pd.testing.assert_frame_equal(
            results_dataframe, expected_results_dataframe, check_dtype=True
        )
        assert results_dataframe["status.status_type"].dtype == "object"
        assert isinstance(results_dataframe["status.status_type"].iloc[0], StatusType)
        assert results_dataframe["started_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["updated_at"].dtype == "datetime64[ns, UTC]"
        assert results_dataframe["file_ids"].dtype == "object"
        assert isinstance(results_dataframe["file_ids"].iloc[0], List)
        assert results_dataframe["keywords"].dtype == "object"
        assert isinstance(results_dataframe["keywords"].iloc[0], List)

    def test__convert_results_to_dataframe_with_id_index__returns_results_dataframe_with_id_index(
        self, results
    ):
        expected_results_dataframe = self.get_expected_results_dataframe(
            results=results
        )
        expected_results_dataframe = expected_results_dataframe.set_index("id")
        expected_result_index = expected_results_dataframe.index.to_list()

        results_dataframe = convert_results_to_dataframe(
            results=results, set_id_as_index=True
        )
        results_index = results_dataframe.index.to_list()

        assert not results_dataframe.empty
        assert isinstance(results_dataframe, pd.DataFrame)
        assert len(results_dataframe) == 3
        assert len(results_dataframe.columns.tolist()) == 19
        assert results_index == expected_result_index
        pd.testing.assert_frame_equal(
            results_dataframe, expected_results_dataframe, check_dtype=True
        )
        assert results_dataframe["status.status_type"].dtype == "object"
        assert isinstance(results_dataframe["status.status_type"].iloc[0], StatusType)
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

    def get_expected_results_dataframe(self, results):
        results_dict = [
            {
                "status": {
                    "status_type": result.status.status_type,
                    "status_name": result.status.status_name,
                },
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
                "properties": result.properties,
                "operator": result.operator,
                "file_ids": result.file_ids,
                "data_table_ids": result.data_table_ids,
                "status_type_summary": result.status_type_summary,
                "workspace": result.workspace,
            }
            for result in results
        ]

        results_df = pd.json_normalize(results_dict, sep=".")
        results_df.dropna(axis="columns", how="all", inplace=True)
        status_type_summary_columns = [
            results_df.pop(column)
            for column in results_df.columns.to_list()
            if column.startswith("status_type_summary.")
        ]
        property_columns = [
            results_df.pop(column)
            for column in results_df.columns.to_list()
            if column.startswith("properties.")
        ]
        results_df = pd.concat(
            [results_df] + status_type_summary_columns + property_columns, axis=1
        )

        return results_df
