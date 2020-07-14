import datetime
import os
import tempfile
import textwrap
from unittest import mock

import mypy.api
import pytest  # type: ignore
from systemlink.clients.tag import DataType, ITagReader
from systemlink.clients.tag._core._serialized_tag_with_aggregates import (
    SerializedTagWithAggregates,
)


class TestITagReader:
    class MockTagReader(ITagReader):
        def __init__(self):
            super().__init__()
            self.mock_read = mock.Mock()

        def _read(self, *args, **kwargs):
            return self.mock_read(*args, **kwargs)

        async def _read_async(self, *args, **kwargs):
            return self.mock_read(*args, **kwargs)

    # data_type: (serialized_value, value)
    test_values = {
        DataType.BOOLEAN: ("True", True),
        DataType.DATE_TIME: (
            "2020-01-01T00:22:11.123456Z",
            datetime.datetime(2020, 1, 1, 0, 22, 11, 123456, datetime.timezone.utc),
        ),
        DataType.DOUBLE: ("1.1", 1.1),
        DataType.INT32: ("-1", -1),
        DataType.UINT64: ("2", 2),
        DataType.STRING: ("foo", "foo"),
    }

    def test__get_tag_reader__read_sends_path_and_data_type(self):
        reader = self.MockTagReader()

        for data_type, (serialized_value, value) in self.test_values.items():
            path = "MyPath.{}".format(data_type.name)
            tag_reader = reader.get_tag_reader(path, data_type)
            reader.mock_read.configure_mock(
                return_value=SerializedTagWithAggregates(
                    path, data_type, serialized_value
                )
            )
            result = tag_reader.read()
            assert reader.mock_read.call_args_list
            assert value == result.value
            assert data_type == result.data_type

    @pytest.mark.asyncio
    async def test__get_tag_reader__read_async_sends_path_and_data_type(self):
        reader = self.MockTagReader()

        for data_type, (serialized_value, value) in self.test_values.items():
            path = "MyPath.{}".format(data_type.name)
            tag_reader = reader.get_tag_reader(path, data_type)
            reader.mock_read.configure_mock(
                return_value=SerializedTagWithAggregates(
                    path, data_type, serialized_value
                )
            )
            result = await tag_reader.read_async()
            assert reader.mock_read.call_args_list
            assert value == result.value
            assert data_type == result.data_type

    @pytest.mark.slow
    def test__get_tag_reader__mypy_ensures_correct_type(self):
        code_template = textwrap.dedent(
            """
            from datetime import datetime
            from systemlink.clients.tag import DataType, ITagReader, TagManager

            def validate_type(val: %s) -> None:
                pass

            mgr = TagManager()
            tag_reader = mgr.get_tag_reader("foo", DataType.%s)
            result = tag_reader.read()
            assert result is not None
            validate_type(result.value)

            """
        )

        # Test successful validation of correct code
        try:
            files = []
            code = {}
            for data_type, (_, value) in self.test_values.items():
                pytype_name = str(type(value).__name__)
                code[data_type.name] = code_template % (pytype_name, data_type.name)
                with tempfile.TemporaryFile(
                    mode="w+", delete=False, prefix=data_type.name + "_", suffix=".py"
                ) as f:
                    files.append(f.name)
                    f.write(code[data_type.name])
            stdout, stderr, exit_code = mypy.api.run(files)
            assert 0 == exit_code, "\n\n".join(
                (stdout, stderr, str(code).replace("\\n", "\n"))
            )
        finally:
            for fname in files:
                os.remove(fname)

        # Test failed validation of incorrect code
        for data_type, (_, value) in self.test_values.items():
            fname = None
            bad_type_name = "bool" if isinstance(value, str) else "str"
            code = code_template % (bad_type_name, data_type.name)
            try:
                with tempfile.TemporaryFile(mode="w+", delete=False) as f:
                    f.write(code)
                stdout, stderr, exit_code = mypy.api.run([f.name])
                assert 0 != exit_code, "\n\n".join((stdout, stderr, code))
            finally:
                if fname is not None:
                    os.remove(fname)
