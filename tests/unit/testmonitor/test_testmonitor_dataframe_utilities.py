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
            status=Status(status_type=StatusType.PASSED),
            id=uuid.uuid1().hex,
            part_number=uuid.uuid1().hex,
            keywords=["keyword1", "keyword2"],
            properties={"property1": "value1", "property2": "value2"},
        ),
        Result(
            status=Status(status_type=StatusType.PASSED),
            id=uuid.uuid1().hex,
            part_number=uuid.uuid1().hex,
            keywords=[],
        ),
        Result(
            status=Status(status_type=StatusType.PASSED),
            id=uuid.uuid1().hex,
            part_number=uuid.uuid1().hex,
            properties={
                "property1": "value1",
                "property2": "value2",
                "property3": "value3",
            },
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
        assert len(results_dataframe) == 3
        assert len(results_dataframe.columns.tolist()) == 7
        assert results_dataframe.equals(expected_results_dataframe)

    def test__convert_results_to_dataframe_with_no_results__returns_empty_dataframe(
        self,
    ):
        results_dataframe = convert_results_to_dataframe(results=[])

        assert isinstance(results_dataframe, pd.DataFrame)
        assert results_dataframe.empty
