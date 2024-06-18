# -*- coding: utf-8 -*-

"""Implementation of HttpConfigurationManager."""

import json
import pathlib
import typing
from typing import Dict, Optional

import yaml
from nisystemlink.clients import core
from nisystemlink.clients.core._internal._http_configuration_file import (
    HttpConfigurationFile,
)
from nisystemlink.clients.core._internal._path_constants import PathConstants


class HttpConfigurationManager:
    """Factory for :class:`HttpConfiguration` objects."""

    HTTP_MASTER_CONFIGURATION_ID = "SYSTEMLINK_MASTER"
    """The default ID of the SystemLink Server's configuration on systems registered using SystemLink Client."""

    HTTP_LOCALHOST_CONFIGURATION_ID = "SYSTEMLINK_LOCALHOST"
    """The default ID of the SystemLink Server's configuration on the SystemLink Server itself."""

    _HTTP_JUPYTER_CONFIGURATION_ID = "SYSTEMLINK_VIRTUAL_JUPYTER"
    """Virtual ID of SystemLink Server's configuration for Jupyter Notebook execution on SLE."""

    _SALT_GRAINS_WORKSPACE_KEY = "systemlink_workspace"
    """Key of Workspace ID stored in the salt grains config file."""

    _configs = None
    _virtual_configs = None

    @classmethod
    def get_configuration(
        cls, id: Optional[str] = None, enable_fallbacks: Optional[bool] = True
    ) -> core.HttpConfiguration:
        """Get the requested or default configuration.

        Args:
            id: The ID of the configuration to find.
            enable_fallbacks: Whether or not to fallback to other known configurations,
                if ``id`` is unavailable.

        Returns:
            The configuration.

        Raises:
            ValueError: if ``id`` is None and ``enable_fallbacks`` is False.
            ApiException: if the specified (or default) configuration is not found.
        """
        if id is not None:
            id = id.upper()
        else:
            if not enable_fallbacks:
                raise ValueError("id cannot be None if enable_fallbacks is False")
            fallback_configuration = cls._fallback()
            if fallback_configuration is None:
                raise core.ApiException("No SystemLink configurations available")
            return fallback_configuration

        if cls._configs is None:
            cls._configs = cls._read_configurations()
        config = cls._configs.get(id)
        if config is not None:
            return config
        if enable_fallbacks:
            fallback_configuration = cls._fallback()
            if fallback_configuration is None:
                raise core.ApiException(
                    "Configuration with ID {!r} was not found, and no ".format(id)
                    + "fallback configurations were available."
                )
            return fallback_configuration
        raise core.ApiException("Configuration with ID {!r} was not found.".format(id))

    @classmethod
    def _fallback(cls) -> Optional[core.HttpConfiguration]:
        """Attempt to acquire fallback HTTP configurations.

        Returns:
            The best available fallback configuration, or None if no such
            configurations are available.
        """
        if cls._configs is None:
            cls._configs = cls._read_configurations()
        if cls._virtual_configs is None:
            cls._virtual_configs = cls._read_virtual_configurations()

        master_config = cls._configs.get(cls.HTTP_MASTER_CONFIGURATION_ID)
        if master_config is not None:
            return master_config
        localhost_config = cls._configs.get(cls.HTTP_LOCALHOST_CONFIGURATION_ID)
        if localhost_config is not None:
            return localhost_config

        jupyter_config = cls._virtual_configs.get(cls._HTTP_JUPYTER_CONFIGURATION_ID)
        if jupyter_config is not None:
            return jupyter_config

        return None

    @classmethod
    def _read_virtual_configurations(cls) -> Dict[str, core.HttpConfiguration]:
        """Loads the virtual HTTP configurations.

        Returns:
            A dictionary mapping each loaded configuration ID to its corresponding
            :class:`HttpConfiguration`.
        """
        configurations = {}  # type: Dict[str, core.HttpConfiguration]
        try:
            configurations[cls._HTTP_JUPYTER_CONFIGURATION_ID] = (
                core.JupyterHttpConfiguration()
            )
        except KeyError:
            # Env variables for Jupyter notebook execution are not available.
            pass

        return configurations

    @classmethod
    def _read_configurations(cls) -> Dict[str, core.HttpConfiguration]:
        """Discover and loads the HTTP configuration files.

        Returns:
            A dictionary mapping each loaded configuration ID to its corresponding
            :class:`HttpConfiguration`.

        Raises:
            ApiException: if multiple configurations with the same ID are simultaneously
                present.
            ApiException: if an OS or permission error prevents reading the directory
                that contains HTTP configurations.
        """
        configurations = {}  # type: Dict[str, core.HttpConfiguration]
        path = cls._http_configurations_directory()
        if not path.exists():
            return configurations
        try:
            json_files = path.glob("*.json")
        except PermissionError as e:
            raise core.ApiException(
                "Not authorized to access HTTP configurations directory: " + str(e)
            )
        except OSError as e:
            raise core.ApiException(
                "Error while accessing HTTP configurations directory: " + str(e)
            )

        workspace = cls._read_system_workspace()

        for json_file in json_files:
            try:
                config_file = cls._read_configuration_file(json_file)
                if config_file is None or config_file.id is None:
                    continue
                if config_file.id in configurations:
                    raise core.ApiException("Duplicate configuration IDs detected.")
                if not config_file.uri:
                    continue

                cert_path = None  # type: Optional[pathlib.Path]
                if config_file.cert_path:
                    cert_path = typing.cast(
                        pathlib.Path,
                        PathConstants.application_data_directory
                        / "Certificates"
                        / config_file.cert_path,
                    )
                    if not cert_path.exists():
                        cert_path = None
                configurations[config_file.id] = core.HttpConfiguration(
                    config_file.uri,
                    config_file.api_key,
                    cert_path=cert_path,
                    workspace=workspace,
                )
            except PermissionError:
                pass
            except OSError:
                # The individual file is inaccessible or badly formatted, so just skip it
                pass
            except json.JSONDecodeError:
                pass
            except ValueError:
                pass
        return configurations

    @classmethod
    def _read_configuration_file(
        cls, path: pathlib.Path
    ) -> Optional[HttpConfigurationFile]:
        """Parse a single SystemLink HTTP configuration file.

        Args:
            path: The path of the file.

        Returns:
            The parsed file, or None if there is no valid configuration present at the
            given path.

        Raises:
            OSError: if an error occurs while accessing the file.
            PermissionError: if the current application does not have permission to
                access the configuration file.
            json.decoder.JSONDecodeError: if the file does not contain valid JSON.
        """
        if not path.exists():
            raise OSError("HTTP configuration file was not found: " + str(path))
        with path.open() as f:
            config_dict = json.load(f)
        config = HttpConfigurationFile.from_json_dict(config_dict)
        if not config.id:
            return None

        config.id = config.id.upper()
        return config

    @classmethod
    def _http_configurations_directory(cls) -> pathlib.Path:
        """Get the platform-specific path to the HTTP Configurations directory.

        Returns:
            pathlib.Path: The path of the HTTP Configurations directory.
        """
        return PathConstants.application_data_directory / "HttpConfigurations"

    @classmethod
    def _salt_grains_path(cls) -> pathlib.Path:
        """Get the SALT grains config file path.

        Returns:
            pathlib.Path: The path of SALT grains config file
        """
        return PathConstants.salt_data_directory / "conf" / "grains"

    @classmethod
    def _read_system_workspace(cls) -> Optional[str]:
        """Get the workspace of the connected remote system.

        Reads workspace from `grains` file of SystemLink Client.

        Returns:
            str: Workspace Id of the remote system.
        """
        salt_grain_file_path = cls._salt_grains_path()

        if salt_grain_file_path.exists():
            with open(salt_grain_file_path, "r", encoding="utf-8") as fp:
                grain_data: Dict = yaml.safe_load(fp)
            return grain_data.get(cls._SALT_GRAINS_WORKSPACE_KEY)

        return None
