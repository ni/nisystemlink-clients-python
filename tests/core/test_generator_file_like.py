from nisystemlink.clients.core.helpers.generator_file_like import GeneratorFileLike


class TestGeneratorFileLike:
    def test__negative_size__read__reads_all_data(self):
        def generate_data():
            yield b"123"
            yield b"456"
            yield b"789"

        generator_file_like = GeneratorFileLike(generate_data())

        assert generator_file_like.read(-1) == b"123456789"

    def test__size_smaller_than_chunk__read__reads_to_size(self):
        def generate_data():
            yield b"1234"

        generator_file_like = GeneratorFileLike(generate_data())

        assert generator_file_like.read(1) == b"1"
        assert generator_file_like.read(2) == b"23"

    def test__size_larger_than_chunk__read__reads_to_size(self):
        def generate_data():
            yield b"123"
            yield b"456789"
            yield b"abcde"

        generator_file_like = GeneratorFileLike(generate_data())

        assert generator_file_like.read(4) == b"1234"
        assert generator_file_like.read(6) == b"56789a"
        assert generator_file_like.read(6) == b"bcde"
