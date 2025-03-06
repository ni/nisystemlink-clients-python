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
            status = Status.PASSED(),
            started_at = "2018-05-07T18:58:05.219692Z",
            updated_at = "2018-05-07T18:58:05.219692Z",
            program_name = "My Program Name",
            id = uuid.uuid1().hex,
            system_id = uuid.uuid1().hex,
            host_name = "host name",
            part_number = uuid.uuid1().hex,
            serial_number = uuid.uuid1().hex,
            total_time_in_seconds = 16.76845106446358,
            keywords = ["keyword1", "keyword2"],
            properties = {"property1": "value1", "property2": "value2"},
            operator = "sample operator",
            file_ids = [uuid.uuid1().hex, uuid.uuid1().hex],
            data_table_ids = [uuid.uuid1().hex, uuid.uuid1().hex],
            status_type_summary = {StatusType.PASSED: 1, StatusType.FAILED: 0},
            workspace = uuid.uuid1().hex,
        ),
    ]

    return results


@pytest.mark.enterprise
class TestTestmonitorDataframeUtilities:
    def test__convert_results_to_dataframe__returns_results_dataframe(self, results):
        expected_results_dict = []
        for result in results:
            expected_results_dict.append(result.dict(exclude_unset=True))
        expected_results_dataframe = pd.json_normalize(expected_results_dict, sep=".")
        expected_results_dataframe.dropna(axis="columns", how="all", inplace=True)

        results_dataframe = convert_results_to_dataframe(results=results)

        assert not results_dataframe.empty
        assert isinstance(results_dataframe, pd.DataFrame)
        assert len(results_dataframe) == 1
        assert len(results_dataframe.columns.tolist()) == 19
        assert results_dataframe.equals(expected_results_dataframe), expected_results_dataframe
        pd.testing.assert_frame_equal(results_dataframe, expected_results_dataframe, check_dtype=True), expected_results_dataframe

    def test__convert_results_to_dataframe_with_no_results__returns_empty_dataframe(
        self,
    ):
        results_dataframe = convert_results_to_dataframe(results=[])

        assert isinstance(results_dataframe, pd.DataFrame)
        assert results_dataframe.empty
