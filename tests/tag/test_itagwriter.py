import datetime
import os
import tempfile
import textwrap
from unittest import mock

import mypy.api
import pytest  # type: ignore
from systemlink.clients.tag import DataType, ITagWriter


class TestITagWriter:
    class MockTagWriter(ITagWriter):
        def __init__(self):
            super().__init__()
            self.mock_write = mock.Mock()

        def _write(self, *args, **kwargs):
            return self.mock_write(*args, **kwargs)

        async def _write_async(self, *args, **kwargs):
            return self.mock_write(*args, **kwargs)

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

    def test__get_tag_writer__write_sends_path_and_data_type(self):
        writer = self.MockTagWriter()

        for data_type, (serialized_value, value) in self.test_values.items():
            path = "MyPath.{}".format(data_type.name)
            tag_writer = writer.get_tag_writer(path, data_type)
            tag_writer.write(value)
            writer.mock_write.assert_called_with(
                path, data_type, serialized_value, None
            )

    @pytest.mark.asyncio
    async def test__get_tag_writer__write_async_sends_path_and_data_type(self):
        writer = self.MockTagWriter()

        for data_type, (serialized_value, value) in self.test_values.items():
            path = "MyPath.{}".format(data_type.name)
            tag_writer = writer.get_tag_writer(path, data_type)
            await tag_writer.write_async(value)
            writer.mock_write.assert_called_with(
                path, data_type, serialized_value, None
            )

    @pytest.mark.slow
    def test__get_tag_writer__mypy_ensures_correct_type(self):
        code_template = textwrap.dedent(
            """
            import datetime
            from systemlink.clients.tag import DataType, TagManager

            value = %s

            mgr = TagManager()
            writer = mgr.create_writer(buffer_size=1)
            tag_writer = writer.get_tag_writer("foo", DataType.%s)
            tag_writer.write(value)
            """
        )

        # Test successful validation of correct code
        try:
            files = []
            code = {}
            for data_type, (_, value) in self.test_values.items():
                code[data_type.name] = code_template % (repr(value), data_type.name)
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

    def test__correct_type__validate_type__doesnt_raise(self):
        ITagWriter._validate_type(True, DataType.BOOLEAN)
        ITagWriter._validate_type(datetime.datetime.now(), DataType.DATE_TIME)
        ITagWriter._validate_type(-1.1, DataType.DOUBLE)
        ITagWriter._validate_type(-1, DataType.DOUBLE)  # an int is valid for DOUBLE
        ITagWriter._validate_type(-1, DataType.INT32)
        ITagWriter._validate_type(2 ** 35, DataType.UINT64)
        ITagWriter._validate_type("", DataType.STRING)

    def test__incorrect_type__validate_type__raises(self):
        bool_val = True
        date_val = datetime.datetime.now()
        dbl_val = 1.1
        int_val = -1
        str_val = ""

        with pytest.raises(ValueError):
            ITagWriter._validate_type(bool_val, DataType.UNKNOWN)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(date_val, DataType.UNKNOWN)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(dbl_val, DataType.UNKNOWN)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(int_val, DataType.UNKNOWN)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(str_val, DataType.UNKNOWN)

        with pytest.raises(ValueError):
            ITagWriter._validate_type(date_val, DataType.BOOLEAN)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(dbl_val, DataType.BOOLEAN)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(int_val, DataType.BOOLEAN)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(str_val, DataType.BOOLEAN)

        with pytest.raises(ValueError):
            ITagWriter._validate_type(bool_val, DataType.DATE_TIME)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(dbl_val, DataType.DATE_TIME)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(int_val, DataType.DATE_TIME)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(str_val, DataType.DATE_TIME)

        with pytest.raises(ValueError):
            ITagWriter._validate_type(bool_val, DataType.DOUBLE)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(date_val, DataType.DOUBLE)
        # Skip int_val: an int is valid for DataType.DOUBLE
        with pytest.raises(ValueError):
            ITagWriter._validate_type(str_val, DataType.DOUBLE)

        with pytest.raises(ValueError):
            ITagWriter._validate_type(bool_val, DataType.INT32)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(date_val, DataType.INT32)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(dbl_val, DataType.INT32)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(str_val, DataType.INT32)

        with pytest.raises(ValueError):
            ITagWriter._validate_type(bool_val, DataType.UINT64)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(date_val, DataType.UINT64)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(dbl_val, DataType.UINT64)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(str_val, DataType.UINT64)

        with pytest.raises(ValueError):
            ITagWriter._validate_type(bool_val, DataType.STRING)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(date_val, DataType.STRING)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(dbl_val, DataType.STRING)
        with pytest.raises(ValueError):
            ITagWriter._validate_type(int_val, DataType.STRING)

    def test__int_out_of_range__validate_type__raises(self):
        with pytest.raises(ValueError) as ex:
            ITagWriter._validate_type(-(2 ** 32 + 1), DataType.INT32)
            assert "range" in ex.message
        with pytest.raises(ValueError) as ex:
            ITagWriter._validate_type(2 ** 32, DataType.INT32)
            assert "range" in ex.message

        with pytest.raises(ValueError) as ex:
            ITagWriter._validate_type(-1, DataType.UINT64)
            assert "range" in ex.message
        with pytest.raises(ValueError) as ex:
            ITagWriter._validate_type(2 ** 64, DataType.UINT64)
            assert "range" in ex.message
