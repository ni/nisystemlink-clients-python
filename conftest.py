# -*- coding: utf-8 -*-

import pytest  # type: ignore
from systemlink.clients import core


def pytest_addoption(parser):
    """Register command line flags that tell us how to connect to the web server.

    Note that command line flags can also be added to the ``[pytest]`` section of
    ``tox.ini``, in an ``addopts`` setting.
    """
    parser.addoption("--cloud-api-key", help="The cloud API key", type=str)
    parser.addoption("--web-server-url", help="The web server's URL", type=str)
    parser.addoption("--web-server-user", help="The web server's user", type=str)
    parser.addoption(
        "--web-server-password", help="The web server's password", type=str
    )


def pytest_collection_modifyitems(items):
    """Modify the collected tests."""
    for item in items:
        # The integration tests are explicitly marked; everything else is a unit test.
        if not list(item.iter_markers("integration")):
            item.add_marker(pytest.mark.unit)


@pytest.fixture(scope="class")
def cloud_config(pytestconfig):
    """Fixture to get a CloudHttpConfiguration for testing.

    This requires the --cloud-api-key command line flag, or else skips the test.
    """
    api_key = pytestconfig.getoption("cloud_api_key", default=None)
    if api_key:
        return core.CloudHttpConfiguration(api_key)
    else:
        pytest.skip("--cloud-api-key setting not found")


@pytest.fixture(scope="class")
def server_config(pytestconfig):
    """Fixture to get an HttpConfiguration for testing.

    This uses the --web-server-url, --web-server-user, and --web-server-password command
    line options, if any are given. If none of them are given, this will try to get the
    default localhost configuration stored in the local Skyline/HttpConfigurations/
    directory. If that is missing, too, the test is skipped.
    """
    settings = {}
    for setting in ("url", "user", "password"):
        val = pytestconfig.getoption("web_server_" + setting, default=None)
        if val:
            settings[setting] = val
    if settings:
        return core.HttpConfiguration(
            settings.get("url", "http://localhost"),
            settings.get("user", "admin"),
            settings.get("password", "admin"),
        )
    try:
        return core.HttpConfigurationManager.get_configuration(
            core.HttpConfigurationManager.HTTP_LOCALHOST_CONFIGURATION_ID, False
        )
    except core.ApiException:
        pytest.skip("--web-server-* settings not found, nor localhost config file")
