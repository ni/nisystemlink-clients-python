# -*- coding: utf-8 -*-

"""Implementation of PathConstants."""

import os
import pathlib
import typing
from typing import Optional

from nisystemlink.clients.core._internal._classproperty_support import (
    ClasspropertySupport,
)
from typing_extensions import final


@final
class PathConstants(metaclass=ClasspropertySupport):
    """Provides file and directory paths for the SystemLink client APIs."""

    COMPANY_NAME = "National Instruments"

    PRODUCT_NAME = "Skyline"

    _application_data_directory = None  # type: Optional[pathlib.Path]

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'PathConstants' is not an acceptable base type")

    def __init__(self) -> None:
        raise TypeError("Can't instantiate static class 'PathConstants'")

    @ClasspropertySupport.classproperty
    def application_data_directory(self) -> pathlib.Path:  # noqa: D401
        """Get the platform-specific path to the common NI Application Data directory.

        Returns:
            The platform-specific path to the common NI Application Data directory.
        """
        if self._application_data_directory is None:
            if os.name == "nt":
                PathConstants._application_data_directory = (
                    self._windows_application_data_directory()
                )
            else:
                PathConstants._application_data_directory = pathlib.Path(
                    "/etc/natinst/niskyline"
                )
        return typing.cast(pathlib.Path, self._application_data_directory)

    @classmethod
    def _windows_application_data_directory(cls) -> pathlib.Path:
        """Get the NI Application Data directory on Windows.

        Returns:
            The NI Application Data directory on Windows.

        Raises:
            RuntimeError: if this method is called on a non-Windows system.
            RuntimeError: if the ProgramData folder cannot be found.
        """
        if os.name != "nt":
            raise RuntimeError("This function is for Windows only")

        try:
            from . import _winpaths

            programdata_dir = pathlib.Path(
                _winpaths.get_path(_winpaths.FOLDERID.ProgramData)
            )
        except Exception:
            programdata_dir = pathlib.Path("C:/ProgramData")
        if not programdata_dir.exists():
            raise RuntimeError("Cannot find ProgramData folder")

        return programdata_dir / cls.COMPANY_NAME / cls.PRODUCT_NAME
