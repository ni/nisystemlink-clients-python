from setuptools import find_namespace_packages, find_packages, setup  # type: ignore
from setuptools.command.test import test as TestCommand  # type: ignore


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # type: ignore

        pytest.main(self.test_args)


pypi_name = "nisystemlink-clients"

packages = find_namespace_packages(include=["systemlink.*"])


def _get_version(name):
    import os

    version = None
    script_dir = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.join(script_dir, name)
    if not os.path.exists(os.path.join(script_dir, "VERSION")):
        version = "0.1.4"
    else:
        with open(os.path.join(script_dir, "VERSION"), "r") as version_file:
            version = version_file.read().rstrip()
    return version


def _read_contents(file_to_read):
    with open(file_to_read, "r") as f:
        return f.read()


setup(
    name=pypi_name,
    version=_get_version(pypi_name),
    description="NI-SystemLink Python API",
    long_description=_read_contents("README.rst"),
    author="National Instruments",
    maintainer="Paul Spangler, Alex Weaver",
    maintainer_email="paul.spangler@ni.com, alex.weaver@ni.com",
    keywords=["nisystemlink", "systemlink"],
    license="MIT",
    packages=packages,
    install_requires=[
        'aenum;python_version<"3.6"',
        "events",
        'httpx;python_version>="3.6"',
        'requests;python_version<"3.6"',
        "typing-extensions",
    ],
    tests_require=["pytest", "pytest-asyncio", "mypy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ],
    cmdclass={"test": PyTest},
    package_data={"": ["VERSION", "*.pyi", "py.typed"]},
)
